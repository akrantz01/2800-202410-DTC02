from collections import Counter

from .model import load_model


def parse_claim_results(results: str) -> list[tuple[str, str]]:
    """
    Parse the results of a claim verification and extraction.

    :param results: The results to parse
    :return: A list of tuples of status and claim
    """
    claims = []

    for result in results.split("\n"):
        result = result.strip()
        if not result:
            continue

        try:
            status, claim = result.split(": ", 1)
        except AttributeError:
            continue

        claims.append((status.lower(), claim))

    return claims


def extract_and_verify_claims(text: str) -> list[tuple[str, str]]:
    """
    Verify the claim using Gemini 1.5.

    :param text: The text to extract claims from and verify
    :return: list of claims and their statuses
    """
    model = load_model()

    response = model.generate_content(text, stream=False)
    return parse_claim_results(response.text)


def calculate_score(results: list[tuple[str, str]]) -> float:
    """
    Calculate the factuality score based on the verification results.

    :param results: A list of verification results
    :return: The factuality score as a percentage
    """
    counts = Counter(map(lambda result: result[0], results))

    determined_claims = counts["true"] + counts["false"]
    if determined_claims == 0:
        return 0.0

    return (counts["true"] / determined_claims) * 100


def determine_accuracy(text: str) -> dict:
    """
    Verify the factuality of an article.

    :param text: The text of the article to analyze
    :return:
    """
    results = extract_and_verify_claims(text)
    score = calculate_score(results)
    return {
        "score": score,
        "claims": list(map(lambda result: {"status": result[0], "claim": result[1]}, results)),
    }
