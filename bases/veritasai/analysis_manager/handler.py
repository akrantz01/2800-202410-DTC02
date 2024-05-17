import functions_framework
from flask import Request, typing
from veritasai.document_id import generate_id
from veritasai.input_validation import AnalyzeText, ValidationError, response_from_validation_error


@functions_framework.http
def handler(request: Request) -> typing.ResponseReturnValue:
    """
    Initiate the analysis process for a document.

    :param request: the incoming request
    :return: an empty successful response
    """
    try:
        body = AnalyzeText.model_validate(request.get_json(silent=True))
    except ValidationError as e:
        return response_from_validation_error(e)

    print(body)

    unique_id = generate_id(body.content, body.author, body.publisher)
    print(unique_id)

    # TODO: check if the document has already been processed
    # TODO: (maybe) save the document to a storage bucket
    # TODO: send pubsub message to analysis worker(s)

    return "", 204
