import functions_framework
from cloudevents.http import CloudEvent
from veritasai.articles import Article
from veritasai.bias import analyze_document, analyze_sentence, get_keyword_sentences
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

    db = get_db()
    document = db.collection("articles").document(article.id)

    bias = analyze_document(text=article.content)

    logger.info("document analysis complete, writing to database")
    document.update(
        {
            "bias": bias,
            "status.bias": "complete",
        }
    )

    logger.info("starting sentence analysis")

    for keyword, sentences in get_keyword_sentences(bias):
        for i, sentence in enumerate(sentences):
            logger.info("processing sentence %d for keyword %s", i, keyword)

            analyze_sentence(sentence)
            document.update({db.field_path("bias", "keywords", keyword, "sentences"): sentences})

    logger.info("sentence analysis complete, writing to database")
    document.update({"status.sentences": "complete"})
