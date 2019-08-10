"""Reduced from Harpo990 handshake"""

from composer.aws.handshake.ssm import SecretManager
from urllib.parse import quote_plus
from typing import *
from copy import deepcopy

def _paths():
    return {
        "aws_key": "s3/aws_key",
        "aws_secret": "s3/aws_secret"
    }

class UnableToAccessParameter(Exception):
    pass

class Handshake:

    # noinspection PyShadowingNames
    def __init__(self, ssm: SecretManager=None, cache: Dict=None):
        """
        Provides authentication secrets. When using in a multiprocessing
        context, should be cloned first for thread safety and to avoid
        AWS throttling.

        :param ssm: AWS System Manager parameter store bindings.
        :param cache: Catalog of pre-retrieved
        """
        assert ssm is not None or cache is not None
        assert ssm is None or cache is None

        if cache is None:
            cache: Dict = {}
        self._cache: Dict = cache

        self._ssm: SecretManager = ssm

    @classmethod
    def build(cls) -> "Handshake":
        ssm: SecretManager = SecretManager("sources")
        return cls(ssm=ssm)

    def _resolve(self, key: str) -> Optional[str]:
        return self._ssm.resolve(key)

    def _get(self, key: str, quote=False) -> str:
        if key not in self._cache:
            self._cache[key] = self._resolve(key)

        value: str = self._cache[key]
        if value is None:
            raise UnableToAccessParameter

        if quote:
            value=quote_plus(value)

        return value

    def clone(self) -> "Handshake":
        self._force()
        cache: dict = deepcopy(self._cache)
        return Handshake(cache=cache)

    def _force(self):
        for key, path in _paths().items():
            if path not in self._cache:
                self._cache[path] = self._ssm.resolve(path)

    # AWS access privileges for various purposes
    def get_aws_key(self) -> str:
        return self._get("s3/aws_key")

    def get_aws_secret(self) -> str:
        return self._get("s3/aws_secret")
