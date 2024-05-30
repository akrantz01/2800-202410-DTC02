import functions_framework
from cloudevents.http import CloudEvent
from veritasai.articles import Article
from veritasai.firebase import get_db
from veritasai.logging import get_logger
from veritasai.summary import GPTSummarizer

logger = get_logger("veritasai.summary_analyzer")


@functions_framework.cloud_event
def handler(event: CloudEvent):
    """
    Summarize a document's content.

    :param event: the incoming event
    """
    article = Article.from_cloud_event(event)
    logger.info("received article %(id)s", {"id": article.id})

    summarizer = GPTSummarizer()
    summary = summarizer.summarize(text=article.content)

    logger.info("summary complete, writing to database")

    get_db().collection("articles").document(article.id).update(
        {
            "summary": summary,
            "status.summary": "complete",
        }
    )
