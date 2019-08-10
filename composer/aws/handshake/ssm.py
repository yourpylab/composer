import boto3
from botocore.exceptions import ClientError
import logging

from typing import *
DEFAULT = "_default"

def _ssm():
    session = boto3.Session(region_name='us-east-1')
    ssm = session.client('ssm')
    return ssm

def _full(profile: str, path: str) -> str:
    return "/Open990/%s/%s" % (profile, path)

def _access_denied(e: ClientError, key: str) -> bool:
    if e.response["Error"]["Code"] == "AccessDeniedException":
        logging.debug("AccessDeniedException accessing '%s'. Could be explicit or by default." % key)
        return True

    return False

def _parameter_not_found(e: ClientError, key: str) -> bool:
    if e.response["Error"]["Code"] == "ParameterNotFound":
        logging.warning("Access explicitly granted to '%s' in IAM but parameter not found" % key)
        return True
    return False

class SecretManager:
    def __init__(self, profile: str):
        self._profile: str = profile
        self._ssm = _ssm()

    def _lookup(self, profile: str, path: str) -> Optional[str]:
        full_path = _full(profile, path)
        logging.debug("Resolved path '%s' for profile '%s' to '%s'." % (path, profile, full_path))
        try:
            value = self._ssm.get_parameter(Name=full_path, WithDecryption=True)
            return value["Parameter"]["Value"]
        except ClientError as e:
            if _access_denied(e, full_path) or _parameter_not_found(e, full_path):
                return None
            raise e

    def resolve(self, path: str) -> Optional[str]:
        logging.info("Attempting to retrieve path '%s' in profile '%s'." % (path, self._profile))
        value: str = self._lookup(self._profile, path)

        if value is None:
            value = self._lookup(DEFAULT, path)

        logging.debug("Received value '%s' for path '%s'." % (value, path))
        return value
