from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class AnalyzeText(BaseModel):
    """
    Input for the analysis-manager service.
    """

    model_config = ConfigDict(alias_generator=lambda name: name.replace("_", "-"))

    content: str = Field(min_length=5)
    author: str = Field(min_length=2)
    publisher: str = Field(min_length=5)
    source_url: HttpUrl
