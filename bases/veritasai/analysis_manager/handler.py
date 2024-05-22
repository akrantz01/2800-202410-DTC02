import functions_framework
from flask import Request, typing
from veritasai.articles import Article
from veritasai.cache import has_article
from veritasai.cors import handle_cors
from veritasai.input_validation import AnalyzeText, ValidationError, response_from_validation_error
from veritasai.pubsub import analysis_requests


@functions_framework.http
@handle_cors
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

    article = Article.from_input(body.content, body.author, body.publisher, body.source_url)

    cached = has_article(article.id)
    if not cached:
        analysis_requests.publish(article)

    return {"id": article.id, "cached": cached}
