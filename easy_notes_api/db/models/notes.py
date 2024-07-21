from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP, UUID
from sqlalchemy.sql import func

from easy_notes_api.db import DeclarativeBase


class Note(DeclarativeBase):
    __tablename__ = "note"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique id of the string in table",
    )
    owner_id = Column(
        "owner_id",
        ForeignKey("user.id"),
        nullable=False,
        doc="Identifier of user, who made note",
    )
    title = Column(
        "title",
        TEXT,
        nullable=False,
        doc="Title of the note.",
    )
    note_text = Column(
        "note_text",
        TEXT,
        nullable=False,
        doc="Main text of the note.",
    )
    comment = Column(
        "comment",
        TEXT,
        nullable=True,
        server_default=None,
        doc="Comment on the note.",
    )
    url = Column(
        "url",
        TEXT,
        nullable=True,
        server_default=None,
        doc="Site that contains text of the note.",
    )
    date_created = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        doc="Date and time of create",
    )
    tag = Column(
        "tag",
        TEXT,
        nullable=True,
        server_default=None,
        doc="Tag of the note.",
    )
    UniqueConstraint(owner_id, title)

    def __repr__(self):
        columns = {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
