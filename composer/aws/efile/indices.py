import json
import logging
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Dict, List, Deque
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

from composer.aws.efile.bucket import EfileBucket
from composer.aws.s3 import Bucket
from composer.efile.structures.metadata import FilingMetadata
from composer.conf import (EARLIEST_YEAR, MAX_WORKERS, INDEX_JSON_NAME,
                           FILING_NAME, DOWNLOAD_TIMEOUT)


def _json_index_key(year: int) -> str:
    return INDEX_JSON_NAME.format(year)

@dataclass
class EfileIndices(Iterable):
    bucket: Bucket

    @classmethod
    def build(cls) -> "EfileIndices":
        bucket: Bucket = EfileBucket()
        return cls(bucket)

    def _get_for_year(self, year: int) -> List[Dict]:
        object_key: str = _json_index_key(year)
        try:
            raw: str = self.bucket.get_obj_body(object_key)
        except FileNotFoundError:
            return []
        as_json: Dict = json.loads(raw)

        # The IRS currently includes a single key in its indices. Blow up if that changes.
        assert len(as_json) == 1
        filing_list_key: str = FILING_NAME.format(year)
        filing_list: List = as_json[filing_list_key]
        return filing_list

    def __iter__(self) -> Iterator[FilingMetadata]:
        years: Iterator = range(EARLIEST_YEAR, datetime.now().year + 1)
        #years: Iterator = range(EARLIEST_YEAR, EARLIEST_YEAR + 1)

        # The IRS currently provides e-files starting with those filed in 2011. Blow up if that changes.
        assert not self.bucket.exists(_json_index_key(EARLIEST_YEAR - 1))
        assert self.bucket.exists(_json_index_key(EARLIEST_YEAR))

        exceptions = list()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_year: Dict[Future, int] = {}
            results: Deque[List[Dict]] = deque()
            for year in years:
                future: Future = executor.submit(self._get_for_year, year)
                future_to_year[future] = year

            for completed_future in as_completed(future_to_year, timeout=DOWNLOAD_TIMEOUT):  # type: Future
                logging.info("Finished downloading index for %i" % future_to_year[completed_future])
                results.append(completed_future.result())

                if completed_future.exception() is not None:
                    exceptions.append(completed_future.exception())
            
        # NOTE: if you want to omit exceptions raising, just
        # comment the folliwng lines of code
        if exceptions:
            raise exceptions.pop()
        

        # NOTE: you can consider to use this outsie with-statemnt
        for result in results:
            for filing_spec in result:
                yield FilingMetadata.from_json(filing_spec)
