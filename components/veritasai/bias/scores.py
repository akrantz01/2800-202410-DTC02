def score_adjectives(analysis: dict) -> float:
    """
    Scores the adjectives in the analysis.

    :param analysis: the scanned analysis
    :return: a float between [0, 1]
    """
    tokens = analysis["syntax"]["tokens"]
    sentences = analysis["syntax"]["sentences"]
    sentence_count = len(sentences)
    high_adjectives = 4 * sentence_count
    if sentence_count == 0:
        return 0
    adjectives = [token["text"] for token in tokens if token["part_of_speech"] == "ADJ"]
    return len(adjectives) / high_adjectives


def count_pronouns(analysis: str) -> dict:
    """
    Counts the he/she pronouns in the analysis.

    :param analysis: a json string of the scanned analysis
    :return: a dictionary with counts of he/she occurances
    """
    tokens = analysis["syntax"]["tokens"]
    pronouns = [token for token in tokens if token["part_of_speech"] == "PRON"]
    try:
        he = [pronoun["lemma"] for pronoun in pronouns if pronoun["lemma"] == "he"]
        she = [pronoun["lemma"] for pronoun in pronouns if pronoun["lemma"] == "she"]
        he_count = len(he)
        she_count = len(she)
    except KeyError:
        he_count = 0
        she_count = 0
    return {"he": he_count, "she": she_count}


def score_pronouns(pronouns: dict) -> float:
    """
    Score the pronouns.

    :param pronouns: a dictionary with counts of he/she occurances
    :return: a float between [0, 1]
    """
    difference = abs(pronouns["he"] - pronouns["she"])
    total = abs(pronouns["he"] + pronouns["she"])
    if total != 0:
        return difference / total
    else:
        return 0


def score_keywords(keywords: dict) -> float:
    """
    Get the overall score for the keywords.

    :param keywords: a dictionary of processed keywords
    :return: a float between [0, 1]
    """
    scores = [abs(keywords[keyword]["sentiment"]["score"]) for keyword in keywords]
    directions = [keywords[keyword]["sentiment"]["label"] for keyword in keywords]
    positive_count = 0
    for direction in directions:
        if direction == "positive":
            positive_count += 1
    negative_count = len(directions) - positive_count
    try:
        direction_score = (positive_count - negative_count) / len(directions)
    except ZeroDivisionError:
        direction_score = 0
    try:
        total_score = sum(scores) / len(scores)
    except ZeroDivisionError:
        total_score = 0
    return {"score": total_score, "direction_bias": direction_score}


def get_relevant_keywords(analysis: dict) -> list[dict]:
    """
    Extract the important keywords from the ai response.

    :param analysis: the scanned analysis
    :return: relevant_keywords as a list of dictionaries
    """
    relevance_cutoff = 0.6

    relevant_keywords = filter(
        lambda entity: (entity["relevance"] >= relevance_cutoff), analysis["keywords"]
    )
    return list(relevant_keywords)


def get_keyword_sentences(keyword: str, sentences: list[dict]) -> list[dict]:
    """
    Extract sentences that contain relevant keyword mentions.

    :param keyword: a keyword found in the text
    :param sentences: a list of sentences:
    :return: a list sentences that contain the keyword
    """
    sentences_with_keywords = []
    sentences_with_keywords += filter(
        lambda sentence: (keyword in sentence["text"] and sentence not in sentences_with_keywords),
        sentences,
    )
    return sentences_with_keywords


def get_overall_relevant_emotions(
    *, analysis: dict | None = None, keyword: dict | None = None
) -> dict:
    """
    Get the relevant emotions from the scanned text.

    relevant emotions are whichever emotion(s) have scored above the threshold.

    :param analysis: the scanned analysis
    :param keyword: extracted keyword, overrides analysis
    :precondition: only one of 'analysis' or 'keyword' must be provided
    """
    relevance_threshold = 0.3
    if keyword:
        emotions = keyword["emotion"]
    else:
        emotions = analysis["emotion"]["document"]["emotion"]

    emotions_copy = emotions.copy()
    for emotion in emotions_copy:
        if emotions_copy[emotion] <= relevance_threshold:
            del emotions[emotion]

    if not emotions:
        return {"neutral": 0}

    emotions["max"] = max(emotions, key=emotions.get)
    # Case for equal
    other_emotions = list(emotions.keys())
    other_emotions.remove("max")
    other_emotions.remove(emotions["max"])
    if other_emotions:
        for emotion in other_emotions:
            if emotions[emotion] == emotions[emotions["max"]]:
                try:
                    emotions["max"].append(emotion)
                except AttributeError:
                    emotions["max"] = [emotions["max"], emotion]

    return emotions


def get_relevant_entities(analysis: dict) -> list[dict]:
    """
    Extract the important entities from the ai response.

    :param analysis: the scanned analysis
    :return: relevant_entities as a list of dictionaries
    """
    relevance_cutoff = 0.6

    entities = analysis["entities"]
    relevant_entities = filter(lambda entity: (entity["relevance"] >= relevance_cutoff), entities)
    return list(relevant_entities)


def get_mention_sentences(confident_mentions: list[dict], sentences: list[dict]) -> list[dict]:
    """
    Extract sentences that contain relevant keyword mentions.

    :param confident_mentions: a list of confident mentions of a keyword
    :param sentences: a list of sentences
    :return: a filtered list of sentences that contain the confident mentions
    """
    mention_locations = map(lambda mention: (mention["location"]), confident_mentions)
    sentences_with_mentions = []
    for mention in mention_locations:
        mention_start = mention[0]
        mention_end = mention[1]
        sentences_with_mentions += filter(
            lambda sentence: (
                (mention_start >= sentence["location"][0])
                and (mention_end <= sentence["location"][1])
                and sentence not in sentences_with_mentions
            ),
            sentences,
        )
    return sentences_with_mentions


def get_confident_mentions(relevant_entity: dict) -> list[dict]:
    """
    Extract the entity mentions from the relevant entities.

    :param relevant_entity: a single relevant entity response from Watson IBM
    :return: a list of confident mention dictionaries
    """
    confidence_cutoff = 0.75

    mentions = relevant_entity["mentions"]
    confident_mentions = filter(
        lambda mention: (mention["confidence"] >= confidence_cutoff), mentions
    )
    return list(confident_mentions)


def process_keywords(analysis: dict) -> dict:
    """
    Process keywords and entities from the analysis.

    Assign emotion, sentiment, and appearing sentences to each keyword and entity.

    :param analysis: the scanned analysis
    :return: a dictionary of keywords, including their sentences, emotion, and sentiment scores
    """
    sentences = analysis["syntax"]["sentences"]
    keywords = get_relevant_keywords(analysis)
    keyword_results = {}
    for keyword in keywords:
        keyword_results[keyword["text"]] = {}
        keyword_results[keyword["text"]]["sentences"] = get_keyword_sentences(
            keyword["text"], sentences
        )
        keyword_results[keyword["text"]]["emotion"] = get_overall_relevant_emotions(keyword=keyword)
        keyword_results[keyword["text"]]["sentiment"] = keyword["sentiment"]
    entities = get_relevant_entities(analysis)
    for entity in entities:
        keyword_results[entity["text"]] = {}
        keyword_results[entity["text"]]["sentences"] = get_mention_sentences(
            get_confident_mentions(entity), sentences
        )
        keyword_results[entity["text"]]["emotion"] = get_overall_relevant_emotions(keyword=entity)
        keyword_results[entity["text"]]["sentiment"] = entity["sentiment"]

    return keyword_results


def get_overall_sentiment(analysis: dict) -> dict:
    """
    Get the overall sentiment from the scanned text.

    :param analysis: the scanned analysis
    :return: the document-level sentiment
    """
    try:
        return analysis["sentiment"]["document"]
    except KeyError:
        return {"score": 0, "label": "neutral"}


def score_segments(segments: dict) -> dict:
    """
    Extract the emotion and sentiment scores for the segments.

    :param segments: a dictionary of sentence segments and scan results
    :return: segment emotion and sentiment results
    """
    segment_scores = {}
    for segment in segments:
        segment_scores[segment] = {}
        segment_scores[segment]["emotion"] = get_overall_relevant_emotions(
            analysis=segments[segment]
        )
        segment_scores[segment]["sentiment"] = get_overall_sentiment(segments[segment])
    return segment_scores
