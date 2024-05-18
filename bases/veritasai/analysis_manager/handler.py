import functions_framework
from flask import Request, typing
from veritasai.articles import Article
from veritasai.cache import has_article
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

    article = Article.from_input(body.content, body.author, body.publisher, body.source_url)

    if has_article(article.id):
        # TODO: return a response indicating that the document has already been processed
        return "", 204

    # TODO: send pubsub message to analysis worker(s)

    return "", 204
