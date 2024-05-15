from typing import List

import functions_framework
from flask import Request, make_response, typing
from pydantic import BaseModel, Field, HttpUrl, ValidationError


class AnalyzeTextAreaModel(BaseModel):
    text_body: str = Field(min_length=10, max_length=1000)
    author_name: List[str] = Field(min_items=1)
    publisher: str = Field(min_length=5)
    source_url: HttpUrl


@functions_framework.http
def handler(request: Request) -> typing.ResponseReturnValue:
    """
    Initiate the analysis process for a document.

    :param request: the incoming request
    :return: an empty successful response
    """
    # TODO: validate incoming request
    try:
        validate_request = AnalyzeTextAreaModel(
            text_body=str(request.form.get("text-to-analyze")),
            author_name=str(request.form.get("author")).split(","),
            publisher=str(request.form.get("publisher")),
            source_url=str(request.form.get("source-url")),
        )
    except ValidationError as e:
        response = make_response({error["type"]: error["msg"] for error in e.errors()})
        return response

    validated_json = validate_request.dict()
    print(validated_json)
    # TODO: (maybe) save the document to a storage bucket
    # TODO: send pubsub message to analysis worker(s)

    return "", 204
