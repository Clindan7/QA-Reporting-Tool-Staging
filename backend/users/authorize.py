from functools import wraps
from jwt import ExpiredSignatureError, DecodeError
from rest_framework.response import Response
from rest_framework import status


import jwt
import logging
from core import settings
from users import user_errors


logger = logging.getLogger(__name__)


def user_authorization(func):
    @wraps(func)
    def authorization(request, *args, **kwargs):
        try:
            token = request.headers["Authorization"]
        except Exception as E:
            logger.exception(E)
            return Response(
                user_errors.AUTHORIZATION_REQUIRED, status=status.HTTP_401_UNAUTHORIZED
            )
        if token:
            try:
                decode = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                request.user_info = decode
                if decode["type"] != "access":
                    return Response(
                        user_errors.INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST
                    )
            except ExpiredSignatureError:
                return Response(
                    user_errors.TOKEN_EXPIRED, status=status.HTTP_401_UNAUTHORIZED
                )
            except DecodeError :
                return Response(
                    user_errors.INVALID_TOKEN, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                user_errors.TOKEN_NOT_FOUND, status=status.HTTP_401_UNAUTHORIZED
            )

        return func(request, *args, **kwargs)

    return authorization
