import dataclasses
from typing import Tuple

import pytest

from composer.efile.structures.filing import Filing

@pytest.fixture
def reference(date_downloaded) -> Filing:
    return Filing(
        record_id="943041314_201012",
        irs_efile_id="201120919349300412",
        irs_dln="93493091004121",
        ein="943041314",
        period="201012",
        name_org="LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST",
        form_type="990",
        date_submitted="2011-09-28",
        date_uploaded="2016-03-21T17:23:53",
        date_downloaded=date_downloaded,
        url="https://s3.amazonaws.com/irs-form-990/201120919349300412_public.xml"
    )

def test_from_json(reference, date_downloaded, filing_original_dict):
    actual: Filing = Filing.from_json(filing_original_dict)
    actual.date_downloaded = date_downloaded  # Too hard to monkeypatch datetime.now
    assert actual == reference

def test_as_tuple(reference: Filing, date_downloaded):
    expected: Tuple = (
        "943041314_201012",
        "201120919349300412",
        "93493091004121",
        "943041314",
        "201012",
        "LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST",
        "990",
        "2011-09-28",
        "2016-03-21T17:23:53",
        date_downloaded,
        "https://s3.amazonaws.com/irs-form-990/201120919349300412_public.xml"
    )
    actual: Tuple = dataclasses.astuple(reference)
    assert actual == expected