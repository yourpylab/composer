from composer.aws.handshake import Handshake
from composer.aws.s3 import AuthenticatedBucket

class EfileBucket(AuthenticatedBucket):
    def __init__(self):
        handshake: Handshake = Handshake.build()
        super().__init__(handshake, "irs-form-990")