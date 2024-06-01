import functions_framework
from cloudevents.http import CloudEvent
from veritasai.accuracy import determine_accuracy
from veritasai.articles import Article
from veritasai.firebase import get_db
from veritasai.logging import get_logger

logger = get_logger("veritasai.accuracy_analyzer")


@functions_framework.cloud_event
def handler(event: CloudEvent):
    """
    Fact-check a document's content.

    :param event: the incoming event
    """
    article = Article.from_cloud_event(event)
    logger.info("received article %(id)s", {"id": article.id})

    accuracy = determine_accuracy(text=article.content)

    logger.info("fact check complete, writing to database")

    get_db().collection("articles").document(article.id).update(
        {
            "accuracy": accuracy,
            "status.accuracy": "complete",
        }
    )
