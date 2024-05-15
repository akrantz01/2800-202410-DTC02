import functions_framework
from flask import Request, make_response, typing
from pydantic import (
    AliasChoices,
    BaseModel,
    Field,
    HttpUrl,
    ValidationError,
)


class AnalyzeTextAreaModel(BaseModel):
    text_body: str = Field(
        min_length=10,
        validation_alias=AliasChoices("text_body", "text-to-analyze"),
    )
    author: str = Field(min_length=1)
    publisher: str = Field(min_length=5)
    source_url: HttpUrl = Field(validation_alias=AliasChoices("source_url", "source-url"))


@functions_framework.http
def handler(request: Request) -> typing.ResponseReturnValue:
    """
    Initiate the analysis process for a document.

    :param request: the incoming request
    :return: an empty successful response
    """
    request_form = {key: request.form[key] for key in request.form}

    # TODO: validate incoming request
    try:
        AnalyzeTextAreaModel.model_validate(request_form)
    except ValidationError as e:
        response = make_response({error["type"]: error["msg"] for error in e.errors()})
        response.status_code = 422
        return response

    request_form["author"] = request_form["author"].split(",")
    # TODO: (maybe) save the document to a storage bucket
    # TODO: send pubsub message to analysis worker(s)

    return "", 204
