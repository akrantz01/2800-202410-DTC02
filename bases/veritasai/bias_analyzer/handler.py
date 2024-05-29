import functions_framework
from cloudevents.http import CloudEvent
from veritasai.articles import Article
from veritasai.bias import analyze
from veritasai.firebase import get_db
from veritasai.logging import get_logger

logger = get_logger("veritasai.bias_analyzer")


@functions_framework.cloud_event
def handler(event: CloudEvent):
    """
    Analyze a document's bias.

    :param event: the incoming event
    """
    article = Article.from_cloud_event(event)
    logger.info("received article %(id)s", {"id": article.id})

    bias = analyze(text=article.content)

    logger.info("analysis complete, writing to database")

    get_db().collection("articles").document(article.id).update(
        {
            "bias": bias,
            "status.bias": "complete",
        }
    )
