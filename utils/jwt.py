import uuid

from django.conf import settings
from django.utils import timezone

import jwt

from .env import get_env_var

DEFAULT_ALGORITHM = "HS256"
API_SECRET_KEY = get_env_var("DJANGO_SECRET_KEY")
API_ISSUER = settings.SIMPLE_JWT["ISSUER"]
DEFAULT_JWT_PAYLOAD_CONTENT = {
    "token_type": "access",
    "exp": timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
    "iat": timezone.now(),
    "jti": uuid.uuid4().hex,
    "iss": API_ISSUER,
}


def decode_jwt(token: str, audience: str):
    payload = jwt.decode(token, key=API_SECRET_KEY, algorithms=[DEFAULT_ALGORITHM], audience=audience)
    return payload


def generate_jwt(payload: dict):
    payload = {**DEFAULT_JWT_PAYLOAD_CONTENT, **payload}
    token = jwt.encode(payload=payload, algorithm=DEFAULT_ALGORITHM, key=API_SECRET_KEY)
    return token
