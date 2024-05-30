import os
import time
from typing import List

import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def extract_claims(text: str) -> List[str]:
    """
    Extract potential claims from the text using OpenAI's model.

    :param text: The text to analyze
    :return: A list of extracted claims
    """
    messages = [
        {"role": "system", "content": "You are an assistant that identifies claims in text."},
        {
            "role": "user",
            "content": 
            f"Identify the claims in the following text:\n\n{text}\n\nPlease provide"
            f"each claim as a separate line without any numerical markers or prefixes.",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=500
    )

    claims_text = response.choices[0].message.content.strip()
    claims = [claim.strip() for claim in claims_text.split("\n") if claim.strip()]
    return claims


def verify_claim(claim: str) -> str:
    """
    Verify the claim using OpenAI's API.

    :param claim: The claim to verify
    :return: The verification result
    """
    messages = [
        {"role": "system", "content": "You are a fact-checking assistant."},
        {
            "role": "user",
            "content": 
            f"Verify the following claim: {claim}\n\nRespond with 'True' or 'False'"
            f"and a brief explanation.",
        },
    ]

    retries = 5
    for i in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            wait_time = 2**i
            time.sleep(wait_time)
        except openai.APIError:
            break
        except Exception:
            break
    return "Error: Unable to verify claim."


def calculate_factuality_score(results: List[str]) -> float:
    """
    Calculate the factuality score based on the verification results.

    :param results: A list of verification results
    :return: The factuality score as a percentage
    """
    total_claims = len(results)
    if total_claims == 0:
        return 0.0
    true_claims = sum(1 for result in results if "True" in result)
    return (true_claims / total_claims) * 100


def verify_article_factuality(text: str) -> float:
    """
    Verify the factuality of an article.

    :param text: The text of the article to analyze
    :return: The factuality score as a percentage
    """
    claims = extract_claims(text)
    results = [verify_claim(claim) for claim in claims]
    factuality_score = calculate_factuality_score(results)
    return factuality_score


def main():
    pass


if __name__ == "__main__":
    main()
