from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator


class NoteForm(BaseModel):
    title: str = Field(examples=["Title of your note"])
    url: HttpUrl | None = Field(
        default=None,
        examples=["http://example.com"],
        description="Here can be url of the existing site or None",
    )
    note_text: str = Field(examples=["Something that you saved"])
    comment: str | None = Field(default=None, examples=["Comment on the note"])
    tag: str | None = Field(
        default=None,
        examples=["Cooking recipe"],
        description="Tag that will help you find specific note",
    )

    @field_validator("url")
    def validate_url(cls, url):
        if url is not None:
            return str(url)


class NoteChangeForm(NoteForm):
    title: str | None = Field(default=None, examples=["Title of your note"])
    note_text: str | None = Field(default=None, examples=["Something that you saved"])


class UserNote(NoteForm):
    date_created: datetime = Field(default=None, examples=["21-07-2024 15:34:45"])

    class Config:
        json_encoders = {
            datetime: lambda t: t.strftime("%d-%m-%Y %H:%M:%S"),
        }


class NoteCreateSuccess(BaseModel):
    message: str
