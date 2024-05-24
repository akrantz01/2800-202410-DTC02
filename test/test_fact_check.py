import unittest
from unittest.mock import patch

from veritasai.fact_check.fact_check import (
    calculate_factuality_score,
    extract_claims,
    fact_check_query,
    is_claim,
    verify_article_factuality,
)


class TestFactCheck(unittest.TestCase):
    def test_extract_claims(self):
        text = "The Earth is flat. Climate change is real!"
        expected_claims = [
            "The Earth is flat.",
            "Climate change is real!",
        ]
        claims = extract_claims(text)
        self.assertEqual(claims, expected_claims)

    def test_is_claim(self):
        claim_sentences = [
            "The Earth is flat.",
            "Climate change is real!",
        ]
        non_claim_sentences = ["The Earth", "Causes", "Real"]
        for sentence in claim_sentences:
            self.assertTrue(is_claim(sentence))
        for sentence in non_claim_sentences:
            self.assertFalse(is_claim(sentence))

    @patch("veritasai.fact_check.fact_check.fact_check_query")
    def test_calculate_factuality_score(self, mock_fact_check_query):
        mock_fact_check_query.side_effect = [
            {
                "claims": [
                    {"text": "The Earth is flat.", "claimReview": [{"textualRating": "False"}]}
                ]
            },
            {
                "claims": [
                    {"text": "Vaccines cause autism.", "claimReview": [{"textualRating": "False"}]}
                ]
            },
            {
                "claims": [
                    {"text": "Climate change is not real!", "claimReview": [{"textualRating": "False"}]}
                ]
            },
        ]
        text = "The Earth is flat. Vaccines cause autism. Climate change is real!"
        claims = extract_claims(text)
        results = [fact_check_query(claim).get("claims", []) for claim in claims]
        results = [item for sublist in results for item in sublist]  # Flatten the list of lists
        factuality_score = calculate_factuality_score(results)
        self.assertEqual(factuality_score, 0)

    @patch("veritasai.fact_check.fact_check.fact_check_query")
    def test_verify_article_factuality(self, mock_fact_check_query):
        mock_fact_check_query.side_effect = [
            {
                "claims": [
                    {"text": "The Earth is flat.", "claimReview": [{"textualRating": "False"}]}
                ]
            },
            {
                "claims": [
                    {"text": "Vaccines cause autism.", "claimReview": [{"textualRating": "False"}]}
                ]
            },
            {
                "claims": [
                    {"text": "Climate change is real!", "claimReview": [{"textualRating": "True"}]}
                ]
            },
        ]
        text = "The Earth is flat. Vaccines cause autism. Climate change is real!"
        score = verify_article_factuality(text)
        self.assertEqual(score, 100.0)


if __name__ == "__main__":
    unittest.main()
