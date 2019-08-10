import json
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Iterator, Dict, List

from composer.aws.efile.bucket import EfileBucket
from composer.aws.s3 import Bucket
from composer.efile.structures.filing import Filing

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

    def _get_for_year(self, year: int) -> Iterator[Filing]:
        object_key: str = _json_index_key(year)
        raw: str = self.bucket.get_obj_body(object_key)
        as_json: Dict = json.loads(raw)

        # The IRS currently includes a single key in its indices. Blow up if that changes.
        assert len(as_json) == 1
        filing_list_key: str = "Filings%i" % year
        filing_list: List = as_json[filing_list_key]
        for filing_spec in filing_list:
            yield Filing.from_json(filing_spec)

    def __iter__(self) -> Iterator[Filing]:
        year: int = EARLIEST_YEAR

        # The IRS currently provides e-files starting with those filed in 2011. Blow up if that changes.
        assert not self.bucket.exists(_json_index_key(year - 1))
        assert self.bucket.exists(_json_index_key(year))

        # TODO Once tests pass, make this concurrent
        while True:
            try:
                logging.info("Attempting to retrieve filings for year %i." % year)
                yield from self._get_for_year(year)
                year += 1
            except FileNotFoundError:
                logging.info("No filings for year %i. Terminating index crawl.")
                break
