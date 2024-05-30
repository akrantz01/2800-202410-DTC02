from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, HttpUrl, field_validator

StringHttpUrl = Annotated[HttpUrl, AfterValidator(str)]


class AnalyzeText(BaseModel):
    """
    Input for the analysis-manager service.
    """

    model_config = ConfigDict(alias_generator=lambda name: name.replace("_", "-"))
    content: str = Field(..., min_length=5)
    author: str = Field(..., min_length=5)
    publisher: str = Field(..., min_length=2)
    source_url: StringHttpUrl | None = None

    @field_validator("author")
    @classmethod
    def disallow_integers(cls, value: str) -> str:
        assert all(not char.isdigit() for char in value), "String must not contain numbers"
        return value
