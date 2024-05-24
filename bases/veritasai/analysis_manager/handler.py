import functions_framework
from flask import Request, jsonify, typing
from google.cloud.firestore import SERVER_TIMESTAMP
from veritasai.articles import Article
from veritasai.authentication import login_required
from veritasai.cache import has_article
from veritasai.cors import handle_cors
from veritasai.fact_check.fact_check import verify_article_factuality
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

    article = Article.from_input(
        content=body.content,
        title=body.title,
        author=body.author,
        publisher=body.publisher,
        url=body.source_url,
    )

    cached = has_article(article.id)

    logger.info("Received article %(id)s for analysis", {"id": article.id, "cached": cached})

    if not cached:
        analysis_requests.publish(article)

        get_db().collection("articles").document(article.id).set(
            {
                "status": {
                    "extract": "pending",
                    "ai": "pending",
                    "accuracy": "pending",
                    "bias": "pending",
                    "tone": "pending",
                    "entities": "pending",
                    "sentences": "pending",
                },
                "title": article.title,
                "author": article.author,
                "publisher": article.publisher,
                "url": article.url,
                "timestamp": SERVER_TIMESTAMP,
            }
        )

    return {"id": article.id, "cached": cached}


@functions_framework.http
@handle_cors
@login_required
def analyze_article(request: Request) -> typing.ResponseReturnValue:
    """
    Analyze the factuality of an article.

    :param request: the incoming request containing article text
    :return: the factuality score as JSON
    """
    try:
        data = request.get_json(silent=True)
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        article_text = data["text"]
        factuality_score = verify_article_factuality(article_text)

        return jsonify({"factuality_score": factuality_score}), 200

    except Exception as e:
        logger.error("Error analyzing article: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500
