from google.cloud import language_v2

# check date of writing vs date of topic
# scan for articles on same topic?
# scan for type of language used
# check if all sides are shown


def analyze_sentiment_sample():
    # Instantiates a client
    client = language_v2.LanguageServiceClient()

    # The text to analyze
    text = "Analyze this text"
    document = language_v2.types.Document(
        content=text, type_=language_v2.types.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    print(f"Text: {text}")
    print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")


analyze_sentiment_sample()
