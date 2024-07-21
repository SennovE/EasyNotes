from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from easy_notes_api.db.connection import get_session
from easy_notes_api.db.models import Note, User
from easy_notes_api.schemas import NoteChangeForm, NoteCreateSuccess, NoteForm, UserNote
from easy_notes_api.utils.enum_exeptions import HttpEnumExceptions
from easy_notes_api.utils.note import (
    add_note_to_db,
    change_title,
    delete_node_by_title,
    get_note,
    is_website_exist,
)
from easy_notes_api.utils.user import get_current_user

api_router = APIRouter(prefix="/note", tags=["Notes"])


@api_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "The title must be unique, but you already have a note with that title",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def create_note(
    note: Annotated[
        NoteForm,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "value": {
                        "title": "Title of your note",
                        "url": "http://example.com",
                        "note_text": "Something that you saved",
                        "comment": "Comment on the note",
                        "tag": "Cooking recipe",
                    },
                },
                "minimal": {
                    "summary": "An example with minimal required data",
                    "value": {
                        "title": "Title of your note",
                        "note_text": "Something that you saved",
                    },
                },
            },
        ),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> NoteCreateSuccess:
    if note.url is not None and not await is_website_exist(note.url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Website with given url doesn't exist",
        )
    new_note = Note(**note.model_dump(exclude_none=True), owner_id=current_user.id)
    await add_note_to_db(new_note, session)
    return {"message": "Created!"}


@api_router.delete(
    "/{note_title}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def delete_note(
    note_title: Annotated[str, Path()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await delete_node_by_title(note_title, current_user, session)


@api_router.put(
    "/{note_title}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "The title must be unique, but you already have a note with that title",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "There is no note with this title",
        },
    },
)
async def rename_note(
    note_title: Annotated[str, Path()],
    changes: Annotated[NoteChangeForm, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await change_title(note_title, changes, current_user, session)


@api_router.get(
    "/{note_title}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
    response_model=UserNote,
)
async def get_note_by_title(
    note_title: Annotated[str, Path()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserNote:
    response = await get_note(note_title, current_user.id, session)
    if response is None:
        raise HttpEnumExceptions.NON_EXISTING_TITLE.value
    return response
