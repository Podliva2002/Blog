from itertools import zip_longest
from typing import Sequence
from typing import List

from sqlalchemy import Table
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    articles: Mapped[List["Article"]] = relationship(back_populates="author")


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=False)
    content: Mapped[str] = mapped_column(String, unique=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped[User] = relationship(back_populates="articles")


def create_tables():
    Base.metadata.create_all(bind=engine)


def insert_data(session: Session):
    session.query(Article).delete()
    session.query(User).delete()
    session.commit()

    users = [
        User(username=username, email=email)
        for username, email in zip_longest(
            ["Nick", "Kolya", "Dmitry"],
            ["Nick@example.com", "Kolya@example.com", "Dmitry@example.com"]
        )
    ]

    session.add_all(users)
    session.commit()

    # Получаем добавленных пользователей
    added_users = session.query(User).all()

    articles = [
        Article(title=title, content=content, author_id=author_id)
        for title, content, author_id in zip_longest(
            ["New world", "Old world", "New technology"],
            ["This is a new world article.", "This is an old world article.", "This is some else article."],
            [user.id for user in added_users]
        )
    ]

    session.add_all(articles)
    session.commit()


def main():
    create_tables()
    with Session(engine) as session:
        insert_data(session)


if __name__ == "__main__":
    main()
