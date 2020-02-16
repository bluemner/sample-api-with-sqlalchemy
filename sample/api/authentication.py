"""
    Authentication
"""
import functools
import random
import string
from datetime import datetime, timedelta

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import request
from werkzeug.exceptions import Unauthorized

from ..settings import get_logger

logger = get_logger(__name__)
class TokenFactory:
    """
        Generates jwt tokens please don't use this in production
        this is only for demo purpose to show of how to test a token key.

        Normally you can get a jwt token from a 3rd party that supports
        open id: Microsoft ADAL, Google, Steam etc.

        Then you will get that 3rd party's public key and use that to decode /
        validate the jwt.

        Also nothing is persistant, which I did on purpose, so each time you
        restart the program a new RSA key will be generated.

        You can verify JWT Key Goto https://jwt.io/. You will need
        to copy the public key, and format so \\n are new lines.
    """
    _raw: str = []
    _tokens: str = []
    logger = get_logger(__name__)
    _audience = 'localhost'

    def __init__(self):
        self._key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend())  # RSA.generate(2048)

        self._private_key: str = self._key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode("utf-8")

        self._public_key: str = self._key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")
        self.logger.debug(
            "Normally you would NEVER log this but as this is a demo:")
        self.logger.debug(self._public_key)
        self.logger.warning("""
    Please don't use Token Factory in production this is only used for
    educational purpose. Each time you start the application a new RSA Key will
    be generated. Hit the open token endpoint to get JWT token.
        """)
        self.logger.warning("")

    def make_token(self) -> str:
        """
            For testing only makes a random token

            .. note ::
                “exp” (Expiration Time) Claim
                “nbf” (Not Before Time) Claim
                “iss” (Issuer) Claim
                “aud” (Audience) Claim
                “iat” (Issued At) Claim
                “jit” (JWT Unique ID) Claim
                “sub” (Subject) Claim
        """
        now = datetime.utcnow()
        time = now + timedelta(seconds=1800)
        value = random.sample(string.digits+string.ascii_letters, 32)

        info = {
            'jti': ''.join(value),
            'exp': time,
            'aud': self._audience,
            'iat': now,
            'nbf': now,
            'iss': '127.0.0.1',
            'sub': 'test-jwt'
        }
        self._raw.append(info)
        jwt_token = jwt.encode(info, self._private_key,
                               algorithm='RS256').decode("utf-8")
        self._tokens.append(jwt_token)
        return jwt_token

    def valid_token(self, token: str) -> bool:
        """ Checks if valid token
        """
        decoded = jwt.decode(token, self._public_key,
                             audience=self._audience, algorithms=['RS256'])
        if decoded in self._raw:
            return True
        return False


_token_factory: TokenFactory = TokenFactory()


def token_validation(func):
    """ Token Validation Decorator
    """
    @functools.wraps(func)
    def wrapper_validate(*args, **kwargs):
        """ Inner wrapper needed for Decorator,

            .. note ::
                args contains self
        """
        try:
            logger.info("Validating Token")
            token = request.headers.environ['HTTP_AUTHORIZATION']
            logger.debug("Testing Token \n\n%s\n\n", token)
            if not _token_factory.valid_token(token):
                raise Unauthorized(f"Invalid token {token}")
        except Exception:
            raise Unauthorized("Invalid token")
        logger.info("Validation was Successfull")
        return func(*args, **kwargs) # This is the calling method
    return wrapper_validate # Inner call from decorator


def user_id() -> int:
    """ Here is where you would do some sort of look up
    """
    return 1
