from flask import Request, Response
from veritasai.config import env

ORIGIN = env.get("CORS_ORIGIN", "*")


def cors_response(request: Request) -> Response:
    """
    Create a CORS response for the given request.

    :param request: the incoming request
    :return: the CORS response
    """
    response = Response(status=204)
    add_cors_headers(response, request)

    return response


def add_cors_headers(response: Response, request: Request):
    """
    Add CORS headers to the given response.

    Modifies the response headers in-place.

    :param response: the response to modify
    :param request: the incoming request
    """

    origin = allowed_origin(request)
    if origin is None:
        return

    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"


def allowed_origin(request: Request) -> str | None:
    """
    Determine the allowed origin.

    Uses the CORS_ORIGIN environment variable when available, otherwise defaults to the request's
    origin.

    :param request: the incoming request
    :return: the allowed origin
    """
    if ORIGIN == "*":
        return request.headers.get("Origin")

    return ORIGIN
