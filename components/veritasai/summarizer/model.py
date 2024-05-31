import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
)

SYSTEM_INSTRUCTIONS = (
    "You are an assistant that provides detailed summaries of text. Summarize the text, focusing "
    "on the main points and key information. Your summaries should be brief, but not lacking in "
    "detail.\n"
    "\n"
    "Users will provide you with a piece of text to summarize and nothing else. You should respond "
    "with the summary and nothing else."
)

_model = None


def load_model() -> GenerativeModel:
    """
    Load a generative model for summarization.

    :return: the model to use
    """
    global _model

    if _model is not None:
        return _model

    vertexai.init()

    _model = GenerativeModel(
        model_name="gemini-1.5-flash-001",
        system_instruction=SYSTEM_INSTRUCTIONS,
        generation_config=GenerationConfig(temperature=1, top_p=0.95, max_output_tokens=512),
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
    )
    return _model
