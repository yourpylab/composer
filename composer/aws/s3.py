import logging
import os

import boto3
from typing import *
from multiprocessing import cpu_count
from mock import MagicMock

from composer.aws.handshake import Handshake
from botocore.errorfactory import ClientError
from botocore.client import Config

logging.getLogger("botocore.vendored.requests.packages.urllib3").setLevel(logging.WARNING)

class Bucket:
    def __init__(self, s3, name: str):
        self.s3 = s3
        self.name = name

    def get_obj_body(self, key: str, encoding: Optional[str]= "utf-8"):
        obj = self.s3.get_object(Bucket=self.name, Key=key)
        encoded = obj['Body'].read()
        if encoding:
            decoded = encoded.decode(encoding)
            return decoded
        return encoded

    # SO 33842944
    def exists(self, key: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.name, Key=key)
            return True
        except ClientError:
            return False

class AuthenticatedBucket(Bucket):
    def __init__(self, handshake: Handshake, bucket_name: str):
        aws_id = handshake.get_aws_key()
        aws_secret = handshake.get_aws_secret()
        config: Config = Config(max_pool_connections=cpu_count() * 10)
        client = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret, config=config)
        super(AuthenticatedBucket, self).__init__(client, bucket_name)

def file_backed_bucket(root_dir: str) -> Bucket:
    """Mock bucket used in tests and fixture creation"""
    bucket: Bucket = MagicMock(spec=Bucket)

    def get_file_content(filename: str, encoding: Optional[str] = "utf-8") -> str:
        filepath: str = os.path.join(root_dir, filename)
        with open(filepath) as fh:
            return fh.read()

    bucket.get_obj_body.side_effect = get_file_content

    def file_exists(filename: str) -> bool:
        filepath: str = os.path.join(root_dir, filename)
        return os.path.exists(filepath)

    bucket.exists.side_effect = file_exists
    return bucket
