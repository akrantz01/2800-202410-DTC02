import os
from typing import List, Optional

import openai
from dotenv import load_dotenv

load_dotenv()


class GPTSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key)

    def _split_text(self, text: str, max_tokens: int = 2048) -> List[str]:
        """
        Split the text into chunks that fit within the token limit.

        :param text: The text to split
        :param max_tokens: The maximum number of tokens per chunk
        :return: A list of text chunks
        """
        words = text.split()
        chunks = []
        chunk = []

        for word in words:
            if len(" ".join(chunk)) + len(word) + 1 > max_tokens:
                chunks.append(" ".join(chunk))
                chunk = []
            chunk.append(word)

        if chunk:
            chunks.append(" ".join(chunk))

        return chunks

    def summarize(self, text: str) -> str:
        """
        Summarize the given text using OpenAI's GPT model.

        :param text: The text to summarize
        :return: The summarized text
        """
        chunks = self._split_text(text)
        summaries = []

        for chunk in chunks:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an assistant that provides detailed summaries of text."
                        "Summarize the text focusing on the main points and key information.",
                    },
                    {
                        "role": "user",
                        "content": f"Text to summarize: {chunk}",
                    },
                ],
                max_tokens=150,
            )

            summary = response.choices[0].message.content.strip()
            summaries.append(summary)

        # Combine summaries into a final summary
        combined_summary = " ".join(summaries)
        return combined_summary

def main():
    return

if __name__ == "__main__":
    main()
    # # Long text string to summarize
    # text = """
    # Your very long text goes here. It can be a multi-paragraph or even a 
    # multi-page text that needs to be summarized. 
    # This text will be split into manageable chunks, each of which will be summarized separately, 
    # and the final result will be a combined summary.
    # """

    # summarizer = GPTSummarizer()
    # summary = summarizer.summarize(text)
    # print("Summary:")
    # print(summary)
