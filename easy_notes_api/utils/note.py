from aiohttp import ClientSession, ClientTimeout
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from easy_notes_api.db.connection import get_session
from easy_notes_api.db.models import Note, User


async def is_website_exist(page_url: str) -> bool:
    timeout = ClientTimeout(total=2.0)
    try:
        async with ClientSession(
            timeout=timeout, connector_owner=False, trust_env=True
        ) as session:
            async with session.get(
                page_url, allow_redirects=False, ssl=False
            ) as response:
                if response.status < 400:
                    return True
    except:
        None
    return False


async def add_note_to_db(new_note: Note, session: AsyncSession) -> None:
    session.add(new_note)
    await session.commit()
