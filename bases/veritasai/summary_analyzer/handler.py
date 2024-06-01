import functions_framework
from cloudevents.http import CloudEvent
from veritasai.articles import Article
from veritasai.firebase import get_db
from veritasai.logging import get_logger
from veritasai.summarizer import summarize

logger = get_logger("veritasai.summary_analyzer")


@functions_framework.cloud_event
def handler(event: CloudEvent):
    """
    Generate a summary of a document.

    :param event: the incoming event
    """
    article = Article.from_cloud_event(event)
    logger.info("received article %(id)s", {"id": article.id})

    summary = summarize(article.content)

    logger.info("summary generation complete, writing to database")

    get_db().collection("articles").document(article.id).update(
        {
            "summary": summary,
            "status.summary": "complete",
        }
    )
