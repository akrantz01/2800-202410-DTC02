from google.cloud import language_v2


def retrieve_sentiment_analysis(text: str):
    """
    Return a JSON object with sentiment for document and its individual sentences.
    :param document: the string to be analyzed
    :return: a dict with nested dictionaries for documentSentiment and Sentences,
            a key named languageCode with a string value and a key named languageSupported
            with a boolean value.
    """
    client = language_v2.LanguageServiceClient()

    # The text to analyze
    document = language_v2.types.Document(
        content=text, type_=language_v2.types.Document.Type.PLAIN_TEXT
    )

    # return the analyzed document
    analyzed_document = client.analyze_sentiment(request={"document": document})

    return analyzed_document
