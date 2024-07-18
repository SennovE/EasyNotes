from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.sql import func

from easy_notes_api.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique id of the string in table",
    )
    username = Column(
        "username",
        TEXT,
        nullable=False,
        unique=True,
        index=True,
        doc="Username for authentication.",
    )
    password_hash = Column(
        "password_hash",
        TEXT,
        nullable=False,
        index=True,
        doc="Hash of user's password",
    )

    def __repr__(self):
        columns = {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
