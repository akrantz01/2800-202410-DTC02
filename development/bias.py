import json

from dotenv import load_dotenv
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    ConceptsOptions,
    EmotionOptions,
    EntitiesOptions,
    Features,
    KeywordsOptions,
    SemanticRolesOptions,
    SentimentOptions,
    SyntaxOptions,
    SyntaxOptionsTokens,
)
from veritasai.config import env
from veritasai.firebase import get_db


def interpret_text(url_input: str = "", text_input: str = "") -> str:
    """
    Interpret text or URL using IBM Watson.

    If text input is give, it will take priority over URL

    :param url_input: a url string
    :param text_input: a text input string
    :return: json string
    """
    load_dotenv()

    authenticator = IAMAuthenticator(env.get("apikey"))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )

    natural_language_understanding.set_service_url(env.get("url"))

    analysis_features = Features(
        concepts=ConceptsOptions(limit=10),
        emotion=EmotionOptions(document=True),
        entities=EntitiesOptions(limit=20, mentions=True, sentiment=True, emotion=True),
        keywords=KeywordsOptions(limit=20, sentiment=True, emotion=True),
        semantic_roles=SemanticRolesOptions(limit=20, keywords=True, entities=True),
        sentiment=SentimentOptions(),
        syntax=SyntaxOptions(
            sentences=True,
            tokens=SyntaxOptionsTokens(lemma=True, part_of_speech=True),
        ),
    )

    if text_input:
        response = natural_language_understanding.analyze(
            text=text_input, features=analysis_features
        ).get_result()
    else:
        analysis_features.metadata = {}
        response = natural_language_understanding.analyze(
            url=url_input, features=analysis_features
        ).get_result()

    return json.dumps(response, indent=2)


def sentence_scan(sentence: str) -> str:
    """
    Interpret relevant sentences using IBM Watson.

    :param text_input: a sentence input string
    :return: json string
    """
    load_dotenv()

    authenticator = IAMAuthenticator(env.get("apikey"))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )

    natural_language_understanding.set_service_url(env.get("url"))

    analysis_features = Features(
        emotion=EmotionOptions(document=True),
        # semantic_roles=SemanticRolesOptions(limit=20, keywords=True, entities=True),
        sentiment=SentimentOptions(),
    )

    response = natural_language_understanding.analyze(
        text=sentence, features=analysis_features
    ).get_result()

    return json.dumps(response, indent=2)


def get_relevant_entities(analysis: str) -> list[dict]:
    """
    Extract the important entities from the ai response.

    :param analysis: json string
    :return: relevant_entities as a list of dictionaries
    """
    relevance_cutoff = 0.6

    ai_analysis = json.loads(analysis)
    entities = ai_analysis["entities"]
    relevant_entities = filter(lambda entity: (entity["relevance"] >= relevance_cutoff), entities)
    return list(relevant_entities)


def get_relevant_keywords(analysis: str) -> list[dict]:
    """
    Extract the important keywords from the ai response.

    :param analysis: json string
    :return: relevant_keywords as a list of dictionaries
    """
    relevance_cutoff = 0.6

    ai_analysis = json.loads(analysis)
    keywords = ai_analysis["keywords"]
    relevant_keywords = filter(lambda entity: (entity["relevance"] >= relevance_cutoff), keywords)
    return list(relevant_keywords)


def get_sentences(analysis: str) -> list[dict]:
    """
    Extract a list of semantically detected sentences.

    :param analysis: json string
    :return: sentences as a list of dictionaries
    """
    ai_analysis = json.loads(analysis)
    sentences = ai_analysis["syntax"]["sentences"]

    return sentences


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


def get_overall_sentiment(analysis: str) -> dict:
    """
    Get the overall sentiment from the scanned text.

    :param analysis: a json string of the scanned analysis
    :return: the document-level sentiment
    """
    ai_analysis = json.loads(analysis)
    return ai_analysis["sentiment"]["document"]


def scan_segments(sentence: str) -> dict:
    """
    Scan the segments of a sentence.

    :param sentence: a sentence
    :return: a dictionary of the segments and their scan results
    """
    minimum_scan_size = 15
    tokens = sentence.split(" ")
    segments_to_scan = []
    current_segment = ""
    for token in tokens:
        if len(current_segment) < minimum_scan_size:
            current_segment += " "
        else:
            segments_to_scan.append(current_segment)
            current_segment = ""

        current_segment += token

    if len(segments_to_scan[-1]) < minimum_scan_size:
        segments_to_scan[-2] = segments_to_scan[-2] + " " + segments_to_scan[-1]

    return {segment: sentence_scan(segment) for segment in segments_to_scan}


def get_segment_scores(segments: dict) -> dict:
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


def get_overall_relevant_emotions(analysis: str = "", keyword=None) -> dict:
    """
    Get the relevant emotions from the scanned text.

    relevant emotions are whichever emotion(s) have scored above the threshold.

    :param analysis: a json string of the scanned analysis
    :param keyword: extracted keyword - option with default None - overrides analysis
    """
    relevance_threshold = 0.3
    if keyword:
        emotions = keyword["emotion"]
    else:
        ai_analysis = json.loads(analysis)
        emotions = ai_analysis["emotion"]["document"]["emotion"]
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


def process_keywords(analysis: str) -> dict:
    """
    Process keywords and entities from the analysis.

    Assign emotion, sentiment, and appearing sentences to each keyword and entity.

    :param analysis: a json string of the scanned analysis
    :return: a dictionary of keywords, including their sentences, emotion, and sentiment scores
    """
    sentences = get_sentences(analysis)
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
    # for keyword in keyword_results:
    # for sentence in keyword_results[keyword]["sentences"]:
    # sentence["scores"] = get_segment_scores(scan_segments(sentence["text"]))
    return keyword_results


def score_adjectives(analysis: str) -> float:
    """
    Scores the adjectives in the analysis.

    :param analysis: a json string of the scanned analysis
    :return: a float between [0, 1]
    """
    ai_analysis = json.loads(analysis)
    tokens = ai_analysis["syntax"]["tokens"]
    sentences = get_sentences(analysis)
    sentence_count = len(sentences)
    high_adjectives = 4 * sentence_count
    adjectives = [token["text"] for token in tokens if token["part_of_speech"] == "ADJ"]
    return len(adjectives) / high_adjectives


def count_pronouns(analysis: str) -> dict:
    """
    Counts the he/she pronouns in the analysis.

    :param analysis: a json string of the scanned analysis
    :return: a dictionary with counts of he/she occurances
    """
    ai_analysis = json.loads(analysis)
    tokens = ai_analysis["syntax"]["tokens"]
    pronouns = [token for token in tokens if token["part_of_speech"] == "PRON"]
    he = [pronoun["lemma"] for pronoun in pronouns if pronoun["lemma"] == "he"]
    she = [pronoun["lemma"] for pronoun in pronouns if pronoun["lemma"] == "she"]
    he_count = len(he)
    she_count = len(she)
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
    direction_score = (positive_count - negative_count) / len(directions)
    total_score = sum(scores) / len(scores)
    return {"score": total_score, "direction_bias": direction_score}


def analyse_bias(
    article_id: str,
    url: str = "",
    text_input: str = "",
    analysis: str = "",
    display_sentence_scores: bool = False,
) -> None:
    """
    Analyse the bias of the text and write to firestore.

    :param article_id: the firestore id of the article
    :param url: the url to be scanned - optional
    :param text_input: the text to be scanned - optional - overrides the url
    :param analysis: a json string of the scanned analysis - optional - overrides text_input and url
    :param display_sentence_scores: boolean indicating sentences should be scored
    """
    if not analysis:
        analysis = interpret_text(url_input=url, text_input=text_input)
    adjective_score = score_adjectives(analysis)
    pronoun_count = count_pronouns(analysis)
    pronoun_score = score_pronouns(pronoun_count)
    keywords = process_keywords(analysis)
    keywords_score = score_keywords(keywords)
    if display_sentence_scores:
        for keyword in keywords:
            for sentence in keywords[keyword]["sentences"]:
                sentence["scores"] = get_segment_scores(scan_segments(sentence["text"]))
    total_score = (adjective_score + pronoun_score + keywords_score["score"]) / 3

    get_db().collection("articles").document(article_id).update(
        {
            "bias": {
                "adjectiveScore": adjective_score,
                "pronounCount": pronoun_count,
                "pronounScore": pronoun_score,
                "keywords": keywords,
                "keywordScore": keywords_score,
                "sentences": display_sentence_scores,
                "biasScore": total_score,
            }
        }
    )


def main():
    """
    Drive the program.
    """
    # my_input = "IBM has one of the largest workforces in the world"
    my_url = (
        "https://www.theonion.com/report-school-shootings-either-way-down-or-too-depress-1851499800"
    )
    analysis = interpret_text(url_input=my_url)
    # print(json.loads(analysis)["keywords"])
    # analysis = interpret_text(text_input=my_input)
    # process_keywords(analysis)
    # score_adjectives(analysis)
    # print(score_keywords(process_keywords(analysis)))
    analyse_bias("gL5po1BLAmwEZ9seMnay", analysis=analysis, display_sentence_scores=True)
    print("done")


if __name__ == "__main__":
    main()
