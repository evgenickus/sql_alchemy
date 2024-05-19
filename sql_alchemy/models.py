from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base, engine

class User(Base):
  __tablename__ = "users"
  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(50), unique=True)
  email: Mapped[str] = mapped_column(String(100), unique=True)
  hashed_password: Mapped[str]

  articles: Mapped[List["Article"]] = relationship(back_populates="author", cascade="all, delete-orphan")

  def __repr__(self) -> str:
    return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, hashad_password={self.hashed_password!r}"


class Article(Base):
  __tablename__= "articles"
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(150))
  content: Mapped[str] = mapped_column(String)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

  author: Mapped["User"] = relationship(back_populates="articles")

  def __repr__(self) -> str:
    return f"Article(id={self.id!r}, title={self.title!r}, content={self.content!r})"

Base.metadata.create_all(bind=engine)
