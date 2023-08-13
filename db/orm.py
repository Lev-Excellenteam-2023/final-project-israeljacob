import os
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from typing import List

db_folder = "db"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "GPT-database.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    uploads: Mapped[List["Upload"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = 'uploads'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(nullable=False)
    upload_time: Mapped[datetime] = mapped_column(nullable=False)
    finish_time: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[List["User"]] = relationship(back_populates="uploads")

    def __repr__(self) -> str:
        return f"Upload(id={self.id!r}, uid={self.uid!r}, filename={self.filename}, upload_time={self.upload_time}, finish_time={self.finish_time}, status={self.status})"

    def upload_path(self):
        return os.path.join('uploads', self.user.email, self.filename)
