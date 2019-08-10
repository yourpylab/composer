from collections.abc import Callable
from composer.efile.structures.filing import Filing
from composer.efile.structures.sqlite import init_sqlite_db
from typing import List, Dict
import datetime

import pytest
import sqlite3

@pytest.fixture()
def empty_db() -> sqlite3.Connection:
    return init_sqlite_db(":memory:")

@pytest.fixture()
def date_downloaded() -> str:
    return "2019-08-07 06:05:04"

@pytest.fixture()
def filing_original_dict() -> Dict:
    return {
        "EIN": "943041314",
        "TaxPeriod": "201012",
        "DLN": "93493091004121",
        "FormType": "990",
        "URL": "https://s3.amazonaws.com/irs-form-990/201120919349300412_public.xml",
        "OrganizationName": "LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST",
        "SubmittedOn": "2011-09-28",
        "ObjectId": "201120919349300412",
        "LastUpdated": "2016-03-21T17:23:53"
    }

@pytest.fixture()
def filing_amended_dict() -> Dict:
    return {
        "EIN": "943041314",
        "TaxPeriod": "201012",
        "DLN": "93493299007301",
        "FormType": "990",
        "URL": "https://s3.amazonaws.com/irs-form-990/201102999349300730_public.xml",
        "OrganizationName": "LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST",
        "SubmittedOn": "2011-11-15",
        "ObjectId": "201102999349300730",
        "LastUpdated": "2016-03-21T17:23:53"
    }

@pytest.fixture()
def dict_to_standard_filing(date_downloaded) -> Callable:
    def ret(filing_dict: Dict) -> Filing:
        filing: Filing = Filing.from_json(filing_dict)
        filing.date_downloaded = date_downloaded
        return filing
    return ret

@pytest.fixture()
def filing_original(filing_original_dict, dict_to_standard_filing) -> Filing:
    return dict_to_standard_filing(filing_original_dict)

@pytest.fixture()
def filing_amended(filing_amended_dict, dict_to_standard_filing) -> Filing:
    return dict_to_standard_filing(filing_amended_dict)
