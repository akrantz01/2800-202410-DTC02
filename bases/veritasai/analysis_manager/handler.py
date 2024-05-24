import functions_framework
from flask import Request, typing
from google.cloud.firestore import SERVER_TIMESTAMP
from veritasai.articles import Article
from veritasai.authentication import login_required
from veritasai.cache import has_article
from veritasai.cors import handle_cors
from veritasai.firebase import get_db
from veritasai.input_validation import AnalyzeText, ValidationError, response_from_validation_error
from veritasai.logging import get_logger
from veritasai.pubsub import analysis_requests

logger = get_logger("veritasai.analysis_manager")


@functions_framework.http
@handle_cors
@login_required
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

    logger.info("Received article %(id)s for analysis", {"id": article.id, "cached": cached})

    if not cached:
        analysis_requests.publish(article)

        get_db().collection("articles").document(article.id).set(
            {
                "status": {
                    "tone": "pending",
                    "bias": "pending",
                    "ai": "pending",
                    "accuracy": "pending",
                    "entities": "pending",
                    "sentences": "pending",
                },
                "author": article.author,
                "publisher": article.publisher,
                "url": article.url,
                "timestamp": SERVER_TIMESTAMP,
            }
        )

    return {"id": article.id, "cached": cached}
