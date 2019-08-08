from dataclasses import dataclass
from typing import Dict
from datetime import datetime

from pytz import timezone

tz = timezone('America/New_York')

FIELD_EQUIVALENTS = {
    "EIN": "ein",
    "TaxPeriod": "period",
    "DLN": "irs_dln",
    "FormType": "form_type",
    "URL": "url",
    "OrganizationName": "name_org",
    "SubmittedOn": "date_submitted",
    "ObjectId": "irs_efile_id",
    "LastUpdated": "date_uploaded"
}

@dataclass
class Filing:
    record_id: str
    irs_efile_id: str
    irs_dln: str
    ein: str
    period: str
    name_org: str
    form_type: str
    date_submitted: str
    date_uploaded: str
    date_downloaded: str
    url: str

    @classmethod
    def from_json(cls, content: Dict) -> "Filing":
        params: Dict = {}
        for irs_key, anr_key in FIELD_EQUIVALENTS.items():
            params[anr_key] = content[irs_key]

        date_downloaded: datetime = datetime.now(tz)
        params["date_downloaded"] = date_downloaded.strftime("%Y-%m-%d %H:%M:%S")
        params["record_id"] = "%s_%s" % (params["ein"], params["period"])
        return cls(**params)
