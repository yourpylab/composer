import logging
from abc import ABC, abstractmethod

import boto3
from typing import *
from datetime import datetime
from composer.aws.handshake import Handshake
import botocore.exceptions

logging.getLogger("botocore.vendored.requests.packages.urllib3").setLevel(logging.WARNING)

def is_notfound(e: botocore.exceptions.ClientError):
    return e.response['Error']['Code'] in ("404", "NoSuchKey")

class S3Resource:
    def __init__(self, id: str, secret: str):
        self.session = boto3.session.Session(
            aws_access_key_id=id,
            aws_secret_access_key=secret
        )

    def s3(self):
        return self.session.resource("s3")

class Bucket:
    def __init__(self, resource: S3Resource, name: str):
        self.s3 = resource.s3()
        self.name = name

    # Boto3 generates s3.Object on the fly, so can't type go obj
    # Also can't figure out how to test the not found functionality
    def _do_with_404(self, key: str, fn: Callable[[Any], Any]) -> Optional[Any]:
        # noinspection PyUnresolvedReferences
        try:
            obj = self.s3.Object(self.name, key)
            return fn(obj)
        except botocore.exceptions.ClientError as e:
            if is_notfound(e):
                return None
            else:
                raise FileNotFoundError("Failed to read key '%s' in bucket '%s'." % (key, self.name)) from e

    def get_size(self, key: str) -> Optional[int]:
        def fn(obj: Any) -> int: return obj.get()['ContentLength']
        return self._do_with_404(key, fn)

    def get_last_modified(self, key: str) -> Optional[datetime]:
        def fn(obj: Any) -> datetime: return obj.last_modified
        return self._do_with_404(key, fn)

    def get_etag(self, key: str) -> Optional[str]:
        def fn(obj: Any) -> str:
            raw = obj.e_tag
            return raw.replace('"', '')
        return self._do_with_404(key, fn)

    def get_obj_body(self, key: str, encoding: Optional[str]= "utf-8"):
        def fn(obj):
            content = obj.get()
            body = content["Body"]
            encoded = body.read()
            if encoding:
                decoded = encoded.decode(encoding)
                return decoded
            return encoded

        return self._do_with_404(key, fn)

    def _filter(self, key: str):
        bucket = self.s3.Bucket(name=self.name)
        objs: List = list(bucket.objects.filter(Prefix=key))
        return objs

    # SO 33842944
    def exists(self, key: str) -> bool:
        objs: List = self._filter(key)
        return len(objs) > 0 and objs[0].key == key

    def list_keys(self) -> List[str]:
        bucket = self.s3.Bucket(name=self.name)
        objects = bucket.objects
        all_objects = objects.all()
        return [resp.key for resp in all_objects]

class AuthenticatedBucket(Bucket):
    def __init__(self, handshake: Handshake, bucket_name: str):
        aws_id = handshake.get_aws_key()
        aws_secret = handshake.get_aws_secret()
        resource = S3Resource(aws_id, aws_secret)
        super(AuthenticatedBucket, self).__init__(resource, bucket_name)
