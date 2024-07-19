from pydantic import BaseModel, field_validator, Field

from easy_notes_api.config import DefaultSettings


class RegistrationForm(BaseModel):
    username: str = Field("your_name", min_length=5, pattern=r"^\S+$")
    password: str = Field("your_password", min_length=8)

    @field_validator("password")
    def validate_password(cls, password):
        password = DefaultSettings().PWD_CONTEXT.hash(password)
        return password


class RegistrationSuccess(BaseModel):
    message: str
