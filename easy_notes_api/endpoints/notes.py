from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from easy_notes_api.db.connection import get_session
from easy_notes_api.db.models import Note, User
from easy_notes_api.schemas import NoteCreateSuccess, NoteForm
from easy_notes_api.utils.note import add_note_to_db, is_website_exist
from easy_notes_api.utils.user import get_current_user

api_router = APIRouter(prefix="/note", tags=["Notes"])


@api_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note: NoteForm,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> NoteCreateSuccess:
    if note.url is not None and not is_website_exist(note.url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Website with given url doesn't exist",
        )
    new_note = Note(**note.model_dump(exclude_none=True), owner_id=current_user.id)
    await add_note_to_db(new_note, session)
    return {"message": "Created!"}
