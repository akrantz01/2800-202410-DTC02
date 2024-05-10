import functions_framework
from flask import Request, typing


@functions_framework.http
def analysis_manager(request: Request) -> typing.ResponseReturnValue:
    """
    Initiate the analysis process for a document.

    :param request: the incoming request
    :return: an empty successful response
    """

    # TODO: validate incoming request
    # TODO: (maybe) save the document to a storage bucket
    # TODO: send pubsub message to analysis worker(s)

    return "", 204
