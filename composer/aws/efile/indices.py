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

EARLIEST_YEAR = 2011

def _json_index_key(year: int) -> str:
    return "index_%i.json" % year

@dataclass
class EfileIndices(Iterable):
    bucket: Bucket

    @classmethod
    def build(cls) -> "EfileIndices":
        bucket: Bucket = EfileBucket()
        return cls(bucket)

    def _get_for_year(self, year: int) -> Iterator[FilingMetadata]:
        object_key: str = _json_index_key(year)
        try:
            raw: str = self.bucket.get_obj_body(object_key)
        except FileNotFoundError:
            return
        as_json: Dict = json.loads(raw)

        # The IRS currently includes a single key in its indices. Blow up if that changes.
        assert len(as_json) == 1
        filing_list_key: str = "Filings%i" % year
        filing_list: List = as_json[filing_list_key]
        for filing_spec in filing_list:
            yield FilingMetadata.from_json(filing_spec)

    def __iter__(self) -> Iterator[FilingMetadata]:
        years: Iterator = range(EARLIEST_YEAR, datetime.now().year + 1)

        # The IRS currently provides e-files starting with those filed in 2011. Blow up if that changes.
        assert not self.bucket.exists(_json_index_key(EARLIEST_YEAR - 1))
        assert self.bucket.exists(_json_index_key(EARLIEST_YEAR))

        with ThreadPoolExecutor() as executor:
            futures: Deque[Future] = deque()
            for year in years:
                future: Future = executor.submit(self._get_for_year, year)
                futures.append(future)
            for completed_future in as_completed(futures):  # type: Future
                yield from completed_future.result()
