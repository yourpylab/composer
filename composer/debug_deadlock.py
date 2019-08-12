import logging

import os
import shutil

from composer.aws.efile.filings import RetrieveEfiles
from composer.aws.efile.indices import EfileIndices
from composer.aws.s3 import Bucket, file_backed_bucket, List
from composer.efile.compose import ComposeEfiles
from composer.efile.update import UpdateEfileState
from composer.fileio.paths import EINPathManager

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

"""Set up test environment"""
BASEPATH: str = os.path.dirname(os.path.abspath(__file__))
fixture_path: str = os.path.join(BASEPATH, "..", "fixtures")
working_path: str = "/tmp/test_composer/efile"
tp1_path = os.path.join(working_path, "first_timepoint")
tp2_path = os.path.join(working_path, "second_timepoint")
shutil.rmtree(working_path, ignore_errors=True)

def make_indices(timepoint: str) -> EfileIndices:
    efile_index_path: str = os.path.join(fixture_path, "efile_indices", "%s_timepoint" % timepoint)
    index_bucket: Bucket = file_backed_bucket(efile_index_path)
    indices: EfileIndices = EfileIndices(index_bucket)
    return indices

def make_compose(tp_path: str) -> ComposeEfiles:
    efile_xml_path: str = os.path.join(fixture_path, "efile_xml")
    xml_bucket: Bucket = file_backed_bucket(efile_xml_path)
    retrieve: RetrieveEfiles = RetrieveEfiles(xml_bucket)
    path_mgr: EINPathManager = EINPathManager(tp_path)
    compose: ComposeEfiles = ComposeEfiles(retrieve, path_mgr)
    return compose

def do_update(timepoint: str, tp_path: str):
    indices: EfileIndices = make_indices(timepoint)
    compose: ComposeEfiles = make_compose(tp_path)
    update: UpdateEfileState = UpdateEfileState(tp_path, indices, compose)
    update()

"""Run the initial update -- no data exists"""
os.makedirs(tp1_path)
do_update("first", tp1_path)

"""Run the second update"""
shutil.copytree(tp1_path, tp2_path)
do_update("second", tp2_path)
