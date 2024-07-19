from pydantic import BaseModel, Field, field_validator

from easy_notes_api.config import DefaultSettings


class RegistrationForm(BaseModel):
    username: str = Field(examples=["your_name"], min_length=5, pattern=r"^\S+$")
    password: str = Field(examples=["your_password"], min_length=8)

    @field_validator("password")
    def validate_password(cls, password):
        password = DefaultSettings().PWD_CONTEXT.hash(password)
        return password


class RegistrationSuccess(BaseModel):
    message: str
