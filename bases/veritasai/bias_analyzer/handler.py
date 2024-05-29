import functions_framework
from cloudevents.http import CloudEvent
from veritasai.articles import Article
from veritasai.bias import analyze
from veritasai.firebase import get_db


@functions_framework.cloud_event
def handler(event: CloudEvent):
    """
    Analyze a document's bias.

    :param event: the incoming event
    """
    article = Article.from_cloud_event(event)

    bias = analyze(text=article.content)

    get_db().collection("articles").document(article.id).update({"bias": bias})
