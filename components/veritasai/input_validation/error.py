from flask import Response, jsonify, make_response
from pydantic import ValidationError


def response_from_validation_error(report: ValidationError) -> Response:
    """
    Create a response from a validation error.

    :param report: the validation error
    :return: the response object
    """
    errors = report.errors(include_input=False, include_context=False, include_url=False)
    response = make_response(jsonify(errors))
    response.status_code = 422
    return response
