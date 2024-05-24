import functools
from typing import Callable

from firebase_admin.auth import InvalidIdTokenError
from flask import Request, make_response, typing
from veritasai.firebase import get_auth
from veritasai.logging import get_logger

logger = get_logger("veritasai.authentication.decorator")


def login_required(
    func: Callable[[Request], typing.ResponseReturnValue],
) -> Callable[[Request], typing.ResponseReturnValue]:
    """
    Decorator to require a user to be logged in.
    """

    @functools.wraps(func)
    def wrapper(request: Request) -> typing.ResponseReturnValue:
        if request.authorization is None or request.authorization.type.lower() != "bearer":
            return make_response({"error": "bearer token required"}, 401)

        try:
            request.user = get_auth().verify_id_token(request.authorization.token)
        except InvalidIdTokenError:
            return make_response({"error": "invalid bearer token"}, 401)

        logger.info("User %(sub)s authenticated", {"sub": request.user["sub"]})
        return func(request)

    return wrapper
