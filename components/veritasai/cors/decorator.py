import functools
from typing import Callable

from flask import Request, make_response, typing

from .response import add_cors_headers, cors_response


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
            return cors_response(request)

        response = make_response(func(request))
        add_cors_headers(response, request)
        return response

    return wrapper
