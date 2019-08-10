from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Iterator, Dict

from composer.efile.xmlio import JsonTranslator
from composer.aws.efile.bucket import EfileBucket
from composer.aws.s3 import Bucket

def _get_filing_key(irs_efile_id: str) -> str:
    return "%s_public.xml" % irs_efile_id

@dataclass
class EfileFilings(Mapping):
    bucket: Bucket
    xml2json: JsonTranslator = field(default_factory=JsonTranslator, init=False)

    @classmethod
    def build(cls) -> "EfileFilings":
        bucket: Bucket = EfileBucket()
        return cls(bucket)

    def __getitem__(self, irs_efile_id: str) -> Dict:
        object_key: str = _get_filing_key(irs_efile_id)
        raw_xml: str = self.bucket.get_obj_body(object_key)
        return self.xml2json(raw_xml)

    def __len__(self) -> int:
        raise AttributeError

    def __iter__(self) -> Iterator:
        raise AttributeError

    def __contains__(self, __x: object) -> bool:
        raise AttributeError
