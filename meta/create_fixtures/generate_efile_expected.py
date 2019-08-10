import os
import json
from typing import Callable, Dict

from composer.aws.s3 import Bucket
from composer.efile.xmlio import JsonTranslator
filings_path: str = "/mnt/dmz/github/analysis/composer/fixtures/efile_xml"
with open("%s/201332289349200818_public.xml" % filings_path) as fh:
    raw_xml = fh.read()
translate: Callable = JsonTranslator()
expected: Dict = translate(raw_xml)
with open("/tmp/expected.json", "w") as fh:
    json.dump(expected, fh, indent=2)
