from aiohttp import ClientSession, ClientTimeout
from fastapi import HTTPException
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from easy_notes_api.db.models import Note, User
from easy_notes_api.schemas import NoteChangeForm

from .enum_exeptions import HttpEnumExceptions


async def is_website_exist(page_url: str) -> bool:
    timeout = ClientTimeout(total=2.0)
    try:
        async with ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(
                page_url, allow_redirects=False, ssl=False
            ) as response:
                if response.status < 400:
                    return True
    except:
        None
    return False


async def get_note(note_title: str, user_id: str, session: AsyncSession) -> Note:
    query = select(Note).where(and_(Note.title == note_title, Note.owner_id == user_id))
    response = await session.scalar(query)
    return response


async def add_note_to_db(new_note: Note, session: AsyncSession) -> None:
    response = await get_note(new_note.title, new_note.owner_id, session)
    if response is not None:
        raise HttpEnumExceptions.NOT_UNIQUE_TITLE.value
    session.add(new_note)
    await session.commit()


async def delete_node_by_title(
    title: str, current_user: User, session: AsyncSession
) -> None:
    query = delete(Note).where(
        and_(Note.title == title, Note.owner_id == current_user.id)
    )
    await session.execute(query)
    await session.commit()


async def change_note_fields(
    note_title: str, changes: NoteChangeForm, current_user: User, session: AsyncSession
) -> None:
    response = await get_note(note_title, current_user.id, session)
    if response is None:
        raise HttpEnumExceptions.NON_EXISTING_TITLE.value
    if current_user.id is not None and await get_note(
        changes.title, current_user.id, session
    ):
        raise HttpEnumExceptions.NOT_UNIQUE_TITLE.value
    for key, value in changes.model_dump(exclude_none=True).items():
        setattr(response, key, value)
    await session.commit()
