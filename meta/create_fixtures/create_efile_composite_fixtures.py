from collections import OrderedDict
from sqlite3 import Connection, connect
from typing import Iterator, Tuple, Dict

from mock import MagicMock

from composer.aws.efile.filings import EfileFilings
from composer.aws.s3 import file_backed_bucket
from composer.efile.compose import ComposeEfiles
from composer.efile.structures.index import EfileMetadataIndex
from composer.efile.structures.metadata import FilingMetadata
from composer.fileio.paths import EINPathManager

BASEPATH = "/dmz/github/analysis/composer/"

def get_composite_items(idx: EfileMetadataIndex) -> Iterator[Tuple[str, Dict[str, FilingMetadata]]]:
    for ein in idx.latest_filings.eins:
        observations: Dict = {o.period : o for o in idx.latest_filings.filings_for_ein(ein)}
        o_sorted: OrderedDict = OrderedDict()
        for period, filing in sorted(zip(observations.keys(), observations.values())):
            o_sorted[period] = filing
        yield ein, o_sorted

for timepoint in ["first", "second"]:
    conn: Connection = connect("%s/fixtures/sqlite/%s_timepoint.sqlite" % (BASEPATH, timepoint))
    index: EfileMetadataIndex = EfileMetadataIndex.build(conn)

    bucket = file_backed_bucket("%s/fixtures/efile_xml" % BASEPATH)
    s3_filings: EfileFilings = EfileFilings(bucket)
    path_mgr: EINPathManager = EINPathManager("%s/fixtures/efile_composites/%s_timepoint" % (BASEPATH, timepoint))

    compose: ComposeEfiles = ComposeEfiles(s3_filings, path_mgr)
    to_record: Iterator = get_composite_items(index)
    compose(to_record)