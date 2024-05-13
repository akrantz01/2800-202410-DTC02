import functions_framework
from flask import Request, typing


@functions_framework.http
def handler(request: Request) -> typing.ResponseReturnValue:
    """
    Check if the submitted document has already been analyzed.

    :param request: the incoming request
    :return: whether the document has already been analyzed
    """

    # TODO: validate incoming request
    # TODO: compute the hash of the document
    # TODO: check if the hash is in the cache
    # TODO: if in cache, return document ID
    # TODO: if not in cache, return False

    return {"cached": False}
