import re
from typing import Dict, List

from googleapiclient.discovery import build
from veritasai.config import env


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
        "claim",
        "said",
        "says",
        "states",
        "state",
        "argues",
        "argue",
        "asserts",
        "assert",
        "believes",
        "believe",
        "contends",
        "contend",
        "maintains",
        "maintain",
        "notes",
        "note",
        "reports",
        "report",
        "indicates",
        "indicate",
        "reveals",
        "reveal",
        "suggests",
        "suggest",
        "implies",
        "imply",
        "declares",
        "declare",
        "mentions",
        "mention",
        "confirms",
        "confirm",
        "denies",
        "deny",
        "acknowledges",
        "acknowledge",
        "recognizes",
        "recognize",
        "agrees",
        "agree",
        "insists",
        "insist",
        "observes",
        "observe",
        "explains",
        "explain",
        "describes",
        "describe",
        "predicts",
        "predict",
        "forecasts",
        "forecast",
        "expects",
        "expect",
        "anticipates",
        "anticipate",
        "proposes",
        "propose",
        "advises",
        "advise",
        "warns",
        "warn",
        "declares",
        "declare",
        "confirms",
        "confirm",
        "admits",
        "admit",
        "affirms",
        "affirm",
        "guarantees",
        "guarantee",
        "testifies",
        "testify",
        "informs",
        "inform",
        "notifies",
        "notify",
        "reveals",
        "reveal",
        "reports",
        "report",
        "mentions",
        "mention",
        "announces",
        "announce",
        "advises",
        "advise",
        "asserts",
        "assert",
        "opines",
        "opine",
        "claims",
        "claim",
        "contends",
        "contend",
        "argues",
        "argue",
        "suggests",
        "suggest",
        "discloses",
        "disclose",
        "implies",
        "imply",
        "hints",
        "hint",
        "alludes",
        "allude",
        "notes",
        "note",
        "remarks",
        "remark",
        "states",
        "state",
        "comments",
        "comment",
        "observes",
        "observe",
        "opines",
        "opine",
        "posits",
        "posit",
        "infers",
        "infer",
        "deduces",
        "deduce",
        "proclaims",
        "proclaim",
        "maintains",
        "maintain",
        "holds",
        "hold",
        "concludes",
        "conclude",
        "verifies",
        "verify",
        "validates",
        "validate",
        "certifies",
        "certify",
        "declares",
        "declare",
        "attests",
        "attest",
        "testifies",
        "testify",
        "swears",
        "swear",
        "affirms",
        "affirm",
        "upholds",
        "uphold",
        "endorses",
        "endorse",
        "supports",
        "support",
        "advocates",
        "advocate",
        "champions",
        "champion",
        "defends",
        "defend",
        "justifies",
        "justify",
        "vindicates",
        "vindicate",
        "proves",
        "prove",
        "demonstrates",
        "demonstrate",
        "exhibits",
        "exhibit",
        "illustrates",
        "illustrate",
        "manifests",
        "manifest",
        "displays",
        "display",
        "shows",
        "show",
        "reveals",
        "reveal",
        "exposes",
        "expose",
        "uncovers",
        "uncover",
        "discloses",
        "disclose",
        "unveils",
        "unveil",
        "clarifies",
        "clarify",
        "explains",
        "explain",
        "elucidates",
        "elucidate",
        "expounds",
        "expound",
        "interprets",
        "interpret",
        "translates",
        "translate",
        "paraphrases",
        "paraphrase",
        "summarizes",
        "summarize",
        "outlines",
        "outline",
        "details",
        "detail",
        "specifies",
        "specify",
        "enumerates",
        "enumerate",
        "lists",
        "list",
        "recites",
        "recite",
        "quotes",
        "quote",
        "recounts",
        "recount",
        "relates",
        "relate",
        "narrates",
        "narrate",
        "depicts",
        "depict",
        "portrays",
        "portray",
        "paints",
        "paint",
        "sketches",
        "sketch",
        "renders",
        "render",
        "captures",
        "capture",
        "frames",
        "frame",
        "affirms",
        "affirm",
        "alleges",
        "allege",
        "announces",
        "announce",
        "anticipates",
        "anticipate",
        "articulates",
        "articulate",
        "ascertains",
        "ascertain",
        "believes",
        "believe",
        "certifies",
        "certify",
        "comments",
        "comment",
        "concedes",
        "concede",
        "concurs",
        "concur",
        "confirms",
        "confirm",
        "contends",
        "contend",
        "declares",
        "declare",
        "demonstrates",
        "demonstrate",
        "discloses",
        "disclose",
        "disputes",
        "dispute",
        "endorses",
        "endorse",
        "explains",
        "explain",
        "expresses",
        "express",
        "finds",
        "find",
        "guarantees",
        "guarantee",
        "holds",
        "hold",
        "hypothesizes",
        "hypothesize",
        "illustrates",
        "illustrate",
        "implies",
        "imply",
        "indicates",
        "indicate",
        "infers",
        "infer",
        "insists",
        "insist",
        "maintains",
        "maintain",
        "mentions",
        "mention",
        "notes",
        "note",
        "observes",
        "observe",
        "opines",
        "opine",
        "points",
        "point",
        "postulates",
        "postulate",
        "proclaims",
        "proclaim",
        "professes",
        "profess",
        "proposes",
        "propose",
        "reaffirms",
        "reaffirm",
        "realizes",
        "realize",
        "reasons",
        "reason",
        "recognizes",
        "recognize",
        "reflects",
        "reflect",
        "reiterates",
        "reiterate",
        "remarks",
        "remark",
        "reports",
        "report",
        "reveals",
        "reveal",
        "states",
        "state",
        "stipulates",
        "stipulate",
        "suggests",
        "suggest",
        "supports",
        "support",
        "supposes",
        "suppose",
        "surmises",
        "surmise",
        "suspects",
        "suspect",
        "swears",
        "swear",
        "testifies",
        "testify",
        "thinks",
        "think",
        "underlines",
        "underline",
        "understands",
        "understand",
        "upholds",
        "uphold",
        "urges",
        "urge",
        "validates",
        "validate",
        "vouches",
        "vouch",
        "warns",
        "warn",
    ]

    # Tokenize the sentence
    words = sentence.lower().split()

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
    service = build("factchecktools", "v1alpha1", developerKey=env.get("GOOGLE_CLOUD_PROJECT"))
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
