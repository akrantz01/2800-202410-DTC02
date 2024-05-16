from flask import Response, make_response
from pydantic import ValidationError


def response_from_validation_error(report: ValidationError) -> Response:
    """
    Create a response from a validation error.

    :param report: the validation error
    :return: the response object
    """
    response = make_response({error["type"]: error["msg"] for error in report.errors()})
    response.status_code = 422
    return response
