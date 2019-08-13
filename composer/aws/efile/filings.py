import json
import logging
import os
import random
import shutil
import string
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Iterator
from functools import lru_cache
from composer.aws.s3 import Bucket, Tuple, Dict, Iterable
from composer.efile.structures.metadata import FilingMetadata
from composer.efile.xmlio import JsonTranslator
from composer.conf import (CACHE_SIZE, MAX_WORKERS, DOWNLOAD_TIMEOUT,
                           PUBLIC_XML_NAME, JSON_FILENAME, UPDATE_TIMEOUT)

# NOTE: magic number moved to settings file 
@lru_cache(maxsize=CACHE_SIZE)
def _ein_path(basepath: str, ein: str) -> str:
    first, second = ein[0:3], ein[3:6]
    ein_path: str = os.path.join(basepath, first, second)
    os.makedirs(ein_path, exist_ok=True)
    return ein_path

def _get_download_targets(changes: Iterable[Tuple[str, Dict[str, FilingMetadata]]], target_path: str) \
        -> Iterator[Tuple[str, str]]:
    for ein, updates in changes:
        ein_path = _ein_path(target_path, ein)
        for filing_md in updates.values():
            irs_efile_id: str = filing_md.irs_efile_id
            yield ein_path, irs_efile_id


# TODO Add lots of timing to this once it's working

def _tmpdir(tmp_base) -> str:
    while True:
        rand_str = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
        dirname: str = os.path.join(tmp_base, rand_str)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            return dirname

class RetrieveEfiles:
    """Download any new e-files as XML from S3 and store them in a temporary directory. Convert them to JSON files, also
    stored in a temporary directory. Yield a map of EIN -> (map of period -> JSON file path)."""

    def __init__(self, bucket: Bucket, tmp_base: str = "/tmp", no_cleanup: bool=False):
        self.bucket: Bucket = bucket
        self.translate = JsonTranslator()
        self.xml_cache_dir: str = _tmpdir(tmp_base)     # Official temp directory package makes things too hard
        self.json_cache_dir: str = _tmpdir(tmp_base)
        self.no_cleanup: bool = no_cleanup

    def _get_json_tuples(self, changes: Iterable[Tuple[str, Dict[str, FilingMetadata]]]) \
            -> Iterator[Tuple[str, Dict[str, str]]]:
        for ein, updates in changes:
            ein_path = _ein_path(self.json_cache_dir, ein)
            json_paths: Dict[str, str] = {}
            for period, filing_md in updates.items():
                irs_efile_id: str = filing_md.irs_efile_id
                json_paths[period] = os.path.join(ein_path, JSON_FILENAME.format(irs_efile_id))
            yield ein, json_paths

    def _convert_all(self, changes: Iterable[Tuple[str, Dict[str, FilingMetadata]]]):
        """Convert all XML files into JSON files. CPU-bound, so process pool."""
        logging.info("Converting XML to JSON.")

        exceptions = list()
        futures = list()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for ein, updates in changes:
                for filing_md in updates.values():
                    irs_efile_id: str = filing_md.irs_efile_id
                    futures.append(executor.submit(self._xml_to_json, ein, irs_efile_id))

            for future in as_completed(futures, timeout=UPDATE_TIMEOUT):
                if future.exception() is not None:
                    exceptions.append(future.exception())
        if exceptions:
            raise exceptions.pop()


    def _xml_to_json(self, ein: str, irs_efile_id: str) -> None:
        xml_path: str = os.path.join(_ein_path(self.xml_cache_dir, ein), PUBLIC_XML_NAME.format(irs_efile_id))
        json_path: str = os.path.join(_ein_path(self.json_cache_dir, ein), JSON_FILENAME.format(irs_efile_id))
        with open(xml_path) as xml_fh, open(json_path, "w") as json_fh:
            raw_xml: str = xml_fh.read()
            as_json: Dict = self.translate(raw_xml)
            json.dump(as_json, json_fh)

    def _download_xml(self, target: Tuple[str, str]):
        ein_path, irs_efile_id = target  # types: str, str
        s3_key: str = PUBLIC_XML_NAME.format(irs_efile_id)
        destination: str = os.path.join(ein_path, s3_key)
        with open(destination, "w") as fh:
            raw_xml: str = self.bucket.get_obj_body(s3_key)
            fh.write(raw_xml)

    def _download_all(self, changes: Iterable[Tuple[str, Dict[str, FilingMetadata]]]):
        """Download all XML files to local storage. I/O-bound, so thread pool."""
        logging.info("Downloading new XML files.")
        
        # NOTE: 1) consider using timeout when downloading files
        # from docs concurrent.futures: 
        # "If timeout is not specified or None, there is no limit to the wait time.""

        exceptions  = list()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            targets: Iterator[Tuple[str, str]] = _get_download_targets(changes, self.xml_cache_dir)
            futures = [executor.submit(self._download_xml, target) for target in targets]

            # NOTE: if timeout is exeeded, TimeoutError exception will raise
            for future in as_completed(futures, timeout=DOWNLOAD_TIMEOUT):
                if future.exception() is not None:
                    exceptions.append(future.exception())

        if exceptions:
            raise exceptions.pop()

    def __call__(self, changes: Iterable[Tuple[str, Dict[str, FilingMetadata]]]) \
            -> Iterator[Tuple[str, Dict[str, str]]]:
        self._download_all(changes)
        self._convert_all(changes)
        # NOTE:  since all tasks are executed within with-statement
        # after exisitng of that statement we can be sure that all 
        # futures are completed. This is due to:
        #https://github.com/python/cpython/blob/9286677538f3cd15aaad7628f4a95ab6aa97536b/Lib/concurrent/futures/_base.py#L623
        #(i.e. wait=True is important)
        yield from self._get_json_tuples(changes)

    def __del__(self):
        if not self.no_cleanup:
            shutil.rmtree(self.xml_cache_dir, ignore_errors=True)
            shutil.rmtree(self.json_cache_dir, ignore_errors=True)
