from pydantic import BaseModel, Field, HttpUrl, field_validator
from url_normalize import url_normalize


class NoteForm(BaseModel):
    url: HttpUrl | None = Field(
        default=None,
        examples=["http://example.com"],
        description="Here can be url of the existing site or None",
    )
    note_text: str = "Something that you saved"
    comment: str = "Comment on the note"

    @field_validator("url")
    def validate_url(cls, url):
        return url_normalize(str(url))


class NoteCreateSuccess(BaseModel):
    message: str
