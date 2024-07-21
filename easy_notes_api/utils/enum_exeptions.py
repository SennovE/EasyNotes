from enum import Enum

from fastapi import HTTPException
from starlette import status


class HttpEnumExceptions(Enum):
    NOT_UNIQUE_TITLE = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The title must be unique, but you already have a note with that title",
    )
    NON_EXISTING_TITLE = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="There is no note with this title",
    )
