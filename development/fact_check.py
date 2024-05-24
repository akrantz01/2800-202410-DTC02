import re
from typing import Dict, List

from googleapiclient.discovery import build


def extract_claims(text: str) -> List[str]:
    """
    Extract potential claims from the text using regex and heuristic rules.

    :param text: The text to analyze
    :return: A list of extracted claims
    """
    sentences = re.split(r"(?<=[.!?]) +", text)
    claims = [sentence for sentence in sentences if is_claim(sentence)]
    return claims


def is_claim(sentence: str) -> bool:
    """
    Heuristic to determine if a sentence is a claim.

    :param sentence: The sentence to evaluate
    :return: True if the sentence is considered a claim, False otherwise
    """
    # Define common assertion verbs
    assertion_verbs = [
        "is",
        "are",
        "was",
        "were",
        "be",
        "being",
        "been",
        "has",
        "have",
        "had",
        "claims",
        "said",
        "states",
        "argues",
        "asserts",
        "believes",
        "contends",
        "maintains",
        "notes",
        "reports",
    ]

    # Tokenize the sentence
    words = sentence.split()

    # Simple heuristic: a sentence is a claim if it contains an assertion verb and is not too short
    return (
        len(words) > 3  # Exclude very short sentences
        and any(verb in words for verb in assertion_verbs)  # Contains an assertion verb
        and sentence[-1] in ".!?"  # Ends with a period, exclamation mark, or question mark
    )


def fact_check_query(query: str) -> dict:
    """
    Query the Google FactCheck API with a given query.

    :param query: The query string to check
    :return: A dictionary with the fact-checking results
    """
    service = build(
        "factchecktools", "v1alpha1", developerKey="AIzaSyCtF2QCk-s0xqwAzswSg8Fj_mdmf0bpsyU"
    )
    request = service.claims().search(query=query)
    response = request.execute()
    return response


def calculate_factuality_score(results: List[Dict]) -> float:
    """
    Calculate the factuality score based on the FactCheck API results.

    :param results: A list of FactCheck API results for claims
    :return: A factuality score between 0 and 100
    """
    total_claims = len(results)
    verified_claims = sum(
        1
        for result in results
        if any(
            review.get("textualRating") in ["True", "False"]
            for review in result.get("claimReview", [])
        )
    )
    if total_claims == 0:
        return 0.0
    factuality_score = (verified_claims / total_claims) * 100
    return factuality_score


def verify_article_factuality(text: str) -> float:
    """
    Verify the factuality of an article.

    :param text: The article text
    :return: A factuality score between 0 and 100
    """
    claims = extract_claims(text)
    results = [fact_check_query(claim).get("claims", []) for claim in claims]
    results = [item for sublist in results for item in sublist]  # Flatten the list of lists
    factuality_score = calculate_factuality_score(results)
    return factuality_score


# Example usage
if __name__ == "__main__":
    article_text = """
    The Earth is flat. Vaccines cause autism. Climate change is not real.
    """  # Replace this with a large text from an actual news article
    score = verify_article_factuality(article_text)
    print(f"Factuality Score: {score}%")
