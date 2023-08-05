# Copyright (C) The Arvados Authors. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

from future import standard_library
standard_library.install_aliases()
from future.utils import  viewvalues, viewitems

import os
import sys
import re
import urllib.parse
from functools import partial
import logging
import json
from collections import namedtuple
from io import StringIO

if os.name == "posix" and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

from schema_salad.sourceline import SourceLine, cmap

from cwltool.command_line_tool import CommandLineTool
import cwltool.workflow
from cwltool.process import scandeps, UnsupportedRequirement, normalizeFilesDirs, shortname, Process
from cwltool.load_tool import fetch_document
from cwltool.pathmapper import adjustFileObjs, adjustDirObjs, visit_class
from cwltool.utils import aslist
from cwltool.builder import substitute
from cwltool.pack import pack
import schema_salad.validate as validate

import arvados.collection
from .util import collectionUUID
import ruamel.yaml as yaml

import arvados_cwl.arvdocker
from .pathmapper import ArvPathMapper, trim_listing
from ._version import __version__
from . import done

logger = logging.getLogger('arvados.cwl-runner')

def trim_anonymous_location(obj):
    """Remove 'location' field from File and Directory literals.

    To make internal handling easier, literals are assigned a random id for
    'location'.  However, when writing the record back out, this can break
    reproducibility.  Since it is valid for literals not have a 'location'
    field, remove it.

    """

    if obj.get("location", "").startswith("_:"):
        del obj["location"]


def remove_redundant_fields(obj):
    for field in ("path", "nameext", "nameroot", "dirname"):
        if field in obj:
            del obj[field]


def find_defaults(d, op):
    if isinstance(d, list):
        for i in d:
            find_defaults(i, op)
    elif isinstance(d, dict):
        if "default" in d:
            op(d)
        else:
            for i in viewvalues(d):
                find_defaults(i, op)

def setSecondary(t, fileobj, discovered):
    if isinstance(fileobj, dict) and fileobj.get("class") == "File":
        if "secondaryFiles" not in fileobj:
            fileobj["secondaryFiles"] = cmap([{"location": substitute(fileobj["location"], sf), "class": "File"} for sf in t["secondaryFiles"]])
            if discovered is not None:
                discovered[fileobj["location"]] = fileobj["secondaryFiles"]
    elif isinstance(fileobj, list):
        for e in fileobj:
            setSecondary(t, e, discovered)

def discover_secondary_files(inputs, job_order, discovered=None):
    for t in inputs:
        if shortname(t["id"]) in job_order and t.get("secondaryFiles"):
            setSecondary(t, job_order[shortname(t["id"])], discovered)

collection_uuid_pattern = re.compile(r'^keep:([a-z0-9]{5}-4zz18-[a-z0-9]{15})(/.*)?$')
collection_pdh_pattern = re.compile(r'^keep:([0-9a-f]{32}\+\d+)(/.*)?')

def upload_dependencies(arvrunner, name, document_loader,
                        workflowobj, uri, loadref_run,
                        include_primary=True, discovered_secondaryfiles=None):
    """Upload the dependencies of the workflowobj document to Keep.

    Returns a pathmapper object mapping local paths to keep references.  Also
    does an in-place update of references in "workflowobj".

    Use scandeps to find $import, $include, $schemas, run, File and Directory
    fields that represent external references.

    If workflowobj has an "id" field, this will reload the document to ensure
    it is scanning the raw document prior to preprocessing.
    """

    loaded = set()
    def loadref(b, u):
        joined = document_loader.fetcher.urljoin(b, u)
        defrg, _ = urllib.parse.urldefrag(joined)
        if defrg not in loaded:
            loaded.add(defrg)
            # Use fetch_text to get raw file (before preprocessing).
            text = document_loader.fetch_text(defrg)
            if isinstance(text, bytes):
                textIO = StringIO(text.decode('utf-8'))
            else:
                textIO = StringIO(text)
            return yaml.safe_load(textIO)
        else:
            return {}

    if loadref_run:
        loadref_fields = set(("$import", "run"))
    else:
        loadref_fields = set(("$import",))

    scanobj = workflowobj
    if "id" in workflowobj:
        # Need raw file content (before preprocessing) to ensure
        # that external references in $include and $mixin are captured.
        scanobj = loadref("", workflowobj["id"])

    sc_result = scandeps(uri, scanobj,
                  loadref_fields,
                  set(("$include", "$schemas", "location")),
                  loadref, urljoin=document_loader.fetcher.urljoin)

    sc = []
    uuids = {}

    def collect_uuids(obj):
        loc = obj.get("location", "")
        sp = loc.split(":")
        if sp[0] == "keep":
            # Collect collection uuids that need to be resolved to
            # portable data hashes
            gp = collection_uuid_pattern.match(loc)
            if gp:
                uuids[gp.groups()[0]] = obj
            if collectionUUID in obj:
                uuids[obj[collectionUUID]] = obj

    def collect_uploads(obj):
        loc = obj.get("location", "")
        sp = loc.split(":")
        if len(sp) < 1:
            return
        if sp[0] in ("file", "http", "https"):
            # Record local files than need to be uploaded,
            # don't include file literals, keep references, etc.
            sc.append(obj)
        collect_uuids(obj)

    visit_class(workflowobj, ("File", "Directory"), collect_uuids)
    visit_class(sc_result, ("File", "Directory"), collect_uploads)

    # Resolve any collection uuids we found to portable data hashes
    # and assign them to uuid_map
    uuid_map = {}
    fetch_uuids = list(uuids.keys())
    while fetch_uuids:
        # For a large number of fetch_uuids, API server may limit
        # response size, so keep fetching from API server has nothing
        # more to give us.
        lookups = arvrunner.api.collections().list(
            filters=[["uuid", "in", fetch_uuids]],
            count="none",
            select=["uuid", "portable_data_hash"]).execute(
                num_retries=arvrunner.num_retries)

        if not lookups["items"]:
            break

        for l in lookups["items"]:
            uuid_map[l["uuid"]] = l["portable_data_hash"]

        fetch_uuids = [u for u in fetch_uuids if u not in uuid_map]

    normalizeFilesDirs(sc)

    if include_primary and "id" in workflowobj:
        sc.append({"class": "File", "location": workflowobj["id"]})

    if "$schemas" in workflowobj:
        for s in workflowobj["$schemas"]:
            sc.append({"class": "File", "location": s})

    def visit_default(obj):
        remove = [False]
        def ensure_default_location(f):
            if "location" not in f and "path" in f:
                f["location"] = f["path"]
                del f["path"]
            if "location" in f and not arvrunner.fs_access.exists(f["location"]):
                # Doesn't exist, remove from list of dependencies to upload
                sc[:] = [x for x in sc if x["location"] != f["location"]]
                # Delete "default" from workflowobj
                remove[0] = True
        visit_class(obj["default"], ("File", "Directory"), ensure_default_location)
        if remove[0]:
            del obj["default"]

    find_defaults(workflowobj, visit_default)

    discovered = {}
    def discover_default_secondary_files(obj):
        discover_secondary_files(obj["inputs"],
                                 {shortname(t["id"]): t["default"] for t in obj["inputs"] if "default" in t},
                                 discovered)

    visit_class(workflowobj, ("CommandLineTool", "Workflow"), discover_default_secondary_files)

    for d in list(discovered):
        # Only interested in discovered secondaryFiles which are local
        # files that need to be uploaded.
        if d.startswith("file:"):
            sc.extend(discovered[d])
        else:
            del discovered[d]

    mapper = ArvPathMapper(arvrunner, sc, "",
                           "keep:%s",
                           "keep:%s/%s",
                           name=name,
                           single_collection=True)

    def setloc(p):
        loc = p.get("location")
        if loc and (not loc.startswith("_:")) and (not loc.startswith("keep:")):
            p["location"] = mapper.mapper(p["location"]).resolved
            return

        if not loc:
            return

        if collectionUUID in p:
            uuid = p[collectionUUID]
            if uuid not in uuid_map:
                raise SourceLine(p, collectionUUID, validate.ValidationException).makeError(
                    "Collection uuid %s not found" % uuid)
            gp = collection_pdh_pattern.match(loc)
            if gp and uuid_map[uuid] != gp.groups()[0]:
                # This file entry has both collectionUUID and a PDH
                # location. If the PDH doesn't match the one returned
                # the API server, raise an error.
                raise SourceLine(p, "location", validate.ValidationException).makeError(
                    "Expected collection uuid %s to be %s but API server reported %s" % (
                        uuid, gp.groups()[0], uuid_map[p[collectionUUID]]))

        gp = collection_uuid_pattern.match(loc)
        if not gp:
            return
        uuid = gp.groups()[0]
        if uuid not in uuid_map:
            raise SourceLine(p, "location", validate.ValidationException).makeError(
                "Collection uuid %s not found" % uuid)
        p["location"] = "keep:%s%s" % (uuid_map[uuid], gp.groups()[1] if gp.groups()[1] else "")
        p[collectionUUID] = uuid

    visit_class(workflowobj, ("File", "Directory"), setloc)
    visit_class(discovered, ("File", "Directory"), setloc)

    if discovered_secondaryfiles is not None:
        for d in discovered:
            discovered_secondaryfiles[mapper.mapper(d).resolved] = discovered[d]

    if "$schemas" in workflowobj:
        sch = []
        for s in workflowobj["$schemas"]:
            sch.append(mapper.mapper(s).resolved)
        workflowobj["$schemas"] = sch

    return mapper


def upload_docker(arvrunner, tool):
    """Uploads Docker images used in CommandLineTool objects."""

    if isinstance(tool, CommandLineTool):
        (docker_req, docker_is_req) = tool.get_requirement("DockerRequirement")
        if docker_req:
            if docker_req.get("dockerOutputDirectory") and arvrunner.work_api != "containers":
                # TODO: can be supported by containers API, but not jobs API.
                raise SourceLine(docker_req, "dockerOutputDirectory", UnsupportedRequirement).makeError(
                    "Option 'dockerOutputDirectory' of DockerRequirement not supported.")
            arvados_cwl.arvdocker.arv_docker_get_image(arvrunner.api, docker_req, True, arvrunner.project_uuid)
        else:
            arvados_cwl.arvdocker.arv_docker_get_image(arvrunner.api, {"dockerPull": "arvados/jobs"}, True, arvrunner.project_uuid)
    elif isinstance(tool, cwltool.workflow.Workflow):
        for s in tool.steps:
            upload_docker(arvrunner, s.embedded_tool)


def packed_workflow(arvrunner, tool, merged_map):
    """Create a packed workflow.

    A "packed" workflow is one where all the components have been combined into a single document."""

    rewrites = {}
    packed = pack(tool.doc_loader, tool.doc_loader.fetch(tool.tool["id"]),
                  tool.tool["id"], tool.metadata, rewrite_out=rewrites)

    rewrite_to_orig = {v: k for k,v in viewitems(rewrites)}

    def visit(v, cur_id):
        if isinstance(v, dict):
            if v.get("class") in ("CommandLineTool", "Workflow"):
                if "id" not in v:
                    raise SourceLine(v, None, Exception).makeError("Embedded process object is missing required 'id' field")
                cur_id = rewrite_to_orig.get(v["id"], v["id"])
            if "location" in v and not v["location"].startswith("keep:"):
                v["location"] = merged_map[cur_id].resolved[v["location"]]
            if "location" in v and v["location"] in merged_map[cur_id].secondaryFiles:
                v["secondaryFiles"] = merged_map[cur_id].secondaryFiles[v["location"]]
            if v.get("class") == "DockerRequirement":
                v["http://arvados.org/cwl#dockerCollectionPDH"] = arvados_cwl.arvdocker.arv_docker_get_image(arvrunner.api, v, True, arvrunner.project_uuid)
            for l in v:
                visit(v[l], cur_id)
        if isinstance(v, list):
            for l in v:
                visit(l, cur_id)
    visit(packed, None)
    return packed


def tag_git_version(packed):
    if tool.tool["id"].startswith("file://"):
        path = os.path.dirname(tool.tool["id"][7:])
        try:
            githash = subprocess.check_output(['git', 'log', '--first-parent', '--max-count=1', '--format=%H'], stderr=subprocess.STDOUT, cwd=path).strip()
        except (OSError, subprocess.CalledProcessError):
            pass
        else:
            packed["http://schema.org/version"] = githash


def upload_job_order(arvrunner, name, tool, job_order):
    """Upload local files referenced in the input object and return updated input
    object with 'location' updated to the proper keep references.
    """

    discover_secondary_files(tool.tool["inputs"], job_order)

    jobmapper = upload_dependencies(arvrunner,
                                    name,
                                    tool.doc_loader,
                                    job_order,
                                    job_order.get("id", "#"),
                                    False)

    if "id" in job_order:
        del job_order["id"]

    # Need to filter this out, gets added by cwltool when providing
    # parameters on the command line.
    if "job_order" in job_order:
        del job_order["job_order"]

    return job_order

FileUpdates = namedtuple("FileUpdates", ["resolved", "secondaryFiles"])

def upload_workflow_deps(arvrunner, tool):
    # Ensure that Docker images needed by this workflow are available

    upload_docker(arvrunner, tool)

    document_loader = tool.doc_loader

    merged_map = {}

    def upload_tool_deps(deptool):
        if "id" in deptool:
            discovered_secondaryfiles = {}
            pm = upload_dependencies(arvrunner,
                                     "%s dependencies" % (shortname(deptool["id"])),
                                     document_loader,
                                     deptool,
                                     deptool["id"],
                                     False,
                                     include_primary=False,
                                     discovered_secondaryfiles=discovered_secondaryfiles)
            document_loader.idx[deptool["id"]] = deptool
            toolmap = {}
            for k,v in pm.items():
                toolmap[k] = v.resolved
            merged_map[deptool["id"]] = FileUpdates(toolmap, discovered_secondaryfiles)

    tool.visit(upload_tool_deps)

    return merged_map

def arvados_jobs_image(arvrunner, img):
    """Determine if the right arvados/jobs image version is available.  If not, try to pull and upload it."""

    try:
        return arvados_cwl.arvdocker.arv_docker_get_image(arvrunner.api, {"dockerPull": img}, True, arvrunner.project_uuid)
    except Exception as e:
        raise Exception("Docker image %s is not available\n%s" % (img, e) )


def upload_workflow_collection(arvrunner, name, packed):
    collection = arvados.collection.Collection(api_client=arvrunner.api,
                                               keep_client=arvrunner.keep_client,
                                               num_retries=arvrunner.num_retries)
    with collection.open("workflow.cwl", "w") as f:
        f.write(json.dumps(packed, indent=2, sort_keys=True, separators=(',',': ')))

    filters = [["portable_data_hash", "=", collection.portable_data_hash()],
               ["name", "like", name+"%"]]
    if arvrunner.project_uuid:
        filters.append(["owner_uuid", "=", arvrunner.project_uuid])
    exists = arvrunner.api.collections().list(filters=filters).execute(num_retries=arvrunner.num_retries)

    if exists["items"]:
        logger.info("Using collection %s", exists["items"][0]["uuid"])
    else:
        collection.save_new(name=name,
                            owner_uuid=arvrunner.project_uuid,
                            ensure_unique_name=True,
                            num_retries=arvrunner.num_retries)
        logger.info("Uploaded to %s", collection.manifest_locator())

    return collection.portable_data_hash()


class Runner(Process):
    """Base class for runner processes, which submit an instance of
    arvados-cwl-runner and wait for the final result."""

    def __init__(self, runner, tool, loadingContext, enable_reuse,
                 output_name, output_tags, submit_runner_ram=0,
                 name=None, on_error=None, submit_runner_image=None,
                 intermediate_output_ttl=0, merged_map=None,
                 priority=None, secret_store=None,
                 collection_cache_size=256,
                 collection_cache_is_default=True):

        super(Runner, self).__init__(tool.tool, loadingContext)

        self.arvrunner = runner
        self.embedded_tool = tool
        self.job_order = None
        self.running = False
        if enable_reuse:
            # If reuse is permitted by command line arguments but
            # disabled by the workflow itself, disable it.
            reuse_req, _ = self.embedded_tool.get_requirement("http://arvados.org/cwl#ReuseRequirement")
            if reuse_req:
                enable_reuse = reuse_req["enableReuse"]
        self.enable_reuse = enable_reuse
        self.uuid = None
        self.final_output = None
        self.output_name = output_name
        self.output_tags = output_tags
        self.name = name
        self.on_error = on_error
        self.jobs_image = submit_runner_image or "arvados/jobs:"+__version__
        self.intermediate_output_ttl = intermediate_output_ttl
        self.priority = priority
        self.secret_store = secret_store

        self.submit_runner_cores = 1
        self.submit_runner_ram = 1024  # defaut 1 GiB
        self.collection_cache_size = collection_cache_size

        runner_resource_req, _ = self.embedded_tool.get_requirement("http://arvados.org/cwl#WorkflowRunnerResources")
        if runner_resource_req:
            if runner_resource_req.get("coresMin"):
                self.submit_runner_cores = runner_resource_req["coresMin"]
            if runner_resource_req.get("ramMin"):
                self.submit_runner_ram = runner_resource_req["ramMin"]
            if runner_resource_req.get("keep_cache") and collection_cache_is_default:
                self.collection_cache_size = runner_resource_req["keep_cache"]

        if submit_runner_ram:
            # Command line / initializer overrides default and/or spec from workflow
            self.submit_runner_ram = submit_runner_ram

        if self.submit_runner_ram <= 0:
            raise Exception("Value of submit-runner-ram must be greater than zero")

        if self.submit_runner_cores <= 0:
            raise Exception("Value of submit-runner-cores must be greater than zero")

        self.merged_map = merged_map or {}

    def job(self,
            job_order,         # type: Mapping[Text, Text]
            output_callbacks,  # type: Callable[[Any, Any], Any]
            runtimeContext     # type: RuntimeContext
           ):  # type: (...) -> Generator[Any, None, None]
        self.job_order = job_order
        self._init_job(job_order, runtimeContext)
        yield self

    def update_pipeline_component(self, record):
        pass

    def done(self, record):
        """Base method for handling a completed runner."""

        try:
            if record["state"] == "Complete":
                if record.get("exit_code") is not None:
                    if record["exit_code"] == 33:
                        processStatus = "UnsupportedRequirement"
                    elif record["exit_code"] == 0:
                        processStatus = "success"
                    else:
                        processStatus = "permanentFail"
                else:
                    processStatus = "success"
            else:
                processStatus = "permanentFail"

            outputs = {}

            if processStatus == "permanentFail":
                logc = arvados.collection.CollectionReader(record["log"],
                                                           api_client=self.arvrunner.api,
                                                           keep_client=self.arvrunner.keep_client,
                                                           num_retries=self.arvrunner.num_retries)
                done.logtail(logc, logger.error, "%s (%s) error log:" % (self.arvrunner.label(self), record["uuid"]), maxlen=40)

            self.final_output = record["output"]
            outc = arvados.collection.CollectionReader(self.final_output,
                                                       api_client=self.arvrunner.api,
                                                       keep_client=self.arvrunner.keep_client,
                                                       num_retries=self.arvrunner.num_retries)
            if "cwl.output.json" in outc:
                with outc.open("cwl.output.json", "rb") as f:
                    if f.size() > 0:
                        outputs = json.loads(f.read().decode())
            def keepify(fileobj):
                path = fileobj["location"]
                if not path.startswith("keep:"):
                    fileobj["location"] = "keep:%s/%s" % (record["output"], path)
            adjustFileObjs(outputs, keepify)
            adjustDirObjs(outputs, keepify)
        except Exception:
            logger.exception("[%s] While getting final output object", self.name)
            self.arvrunner.output_callback({}, "permanentFail")
        else:
            self.arvrunner.output_callback(outputs, processStatus)
