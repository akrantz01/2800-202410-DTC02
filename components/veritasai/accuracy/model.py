import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
)

SYSTEM_INSTRUCTIONS = (
    "You are an assistant who helps check factual information. Give your best estimation of "
    "whether a claim is accurate.\n"
    "\n"
    "You will receive a piece of text as input. Your goal is to identify all claims in the text "
    "and then report the actuality of the claim. For each claim you identify, you should respond "
    'in the form "<status>: <claim>" where <status> is either "True", "False", or '
    '"Unknown", and <claim> is the identified claim. Separate each status-claim pair with two '
    "newlines."
)

_model = None


def load_model() -> GenerativeModel:
    """
    Load a generative model for fact checking.

    :return: the model to use
    """
    global _model

    if _model is not None:
        return _model

    vertexai.init()

    _model = GenerativeModel(
        model_name="gemini-1.5-flash-001",
        system_instruction=SYSTEM_INSTRUCTIONS,
        generation_config=GenerationConfig(temperature=1, top_p=0.95, max_output_tokens=1024),
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
    )
    return _model
