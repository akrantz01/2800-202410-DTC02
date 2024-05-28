import functions_framework
from cloudevents.http import CloudEvent
from veritasai.articles import Article
from veritasai.firebase import get_db
from veritasai.tone import analyze


@functions_framework.cloud_event
def handler(event: CloudEvent):
    """
    Analyze a document's tone.

    :param event: the incoming event
    """
    article = Article.from_cloud_event(event)

    tone = analyze(text=article.content)

    get_db().collection("articles").document(article.id).update({"tone": tone})
