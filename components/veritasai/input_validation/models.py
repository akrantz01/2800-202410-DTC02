from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class AnalyzeText(BaseModel):
    """
    Input for the analysis-manager service.
    """

    model_config = ConfigDict(alias_generator=lambda name: name.replace("_", "-"))

    text_body: str = Field(min_length=10)
    author: str = Field(min_length=1)
    publisher: str = Field(min_length=5)
    source_url: HttpUrl
