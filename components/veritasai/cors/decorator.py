import functools
from typing import Callable

from flask import Request, make_response, typing
from veritasai.logging import get_logger

from .response import add_cors_headers, cors_response

logger = get_logger("veritasai.cors.decorator")


def handle_cors(
    func: Callable[[Request], typing.ResponseReturnValue],
) -> Callable[[Request], typing.ResponseReturnValue]:
    """
    Wrap a function to handle CORS requests.

    :param func: the function to wrap
    :return: the wrapped function
    """

    @functools.wraps(func)
    def wrapper(request: Request) -> typing.ResponseReturnValue:
        if request.method == "OPTIONS":
            logger.info("Handling CORS preflight request")
            return cors_response(request)

        response = make_response(func(request))
        add_cors_headers(response, request)
        return response

    return wrapper
