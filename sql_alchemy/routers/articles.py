from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from .dependencies import get_db
from .auth import get_current_user
from enum import Enum


router = APIRouter()


articles = list()


def pull_articles(db: Session = Depends(get_db)):
  global articles
  titles = crud.get_titles(db)
  articles = [t[0] for t in titles]
  return articles

Animal = Enum('Animal', {el:el for el in articles}, type=str)

@router.get("/", response_model=List[schemas.ArticleBase])
def read_articles(db: Session = Depends(get_db)):
  print(pull_articles(db))
  return crud.get_articles(db)

@router.get("/title", response_model=List[schemas.ArticleBase])
def search_articles_by_title(title: str, db: Session = Depends(get_db)):
  return crud.search_article_like_title(db, title)

@router.get("/username", response_model=List[schemas.ArticleBase])
def search_articles_by_username(username: str, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_username(db, username)
  articles = crud.select_article_by_user_id(db, user_id=db_user.id)
  return articles

@router.post("/", response_model=schemas.ArticleBase)
def add_article(
  title: str,
  content: str = Body(..., title="Article Content"),
  db: Session = Depends(get_db),
  current_user: schemas.UserBase = Depends(get_current_user)
  ):
  db_user = crud.get_user_by_username(db, current_user.username)
  if db_user is None:
    raise HTTPException(status_code=404, detail=f"User: '{current_user.username}' does not exists")
  article = schemas.ArticleCreate(title=title, content=content, user_id=db_user.id)
  return crud.create_article(db, article, current_user.username)

@router.patch("/", response_model=schemas.ArticleBase)
def edit_article(
  title: Animal,
  content: str = Body(..., title="Article Content"),
  db: Session = Depends(get_db),
  current_user: schemas.UserBase = Depends(get_current_user),
  ):
  db_user = crud.get_user_by_username(db, current_user.username)
  if db_user is None:
    raise HTTPException(status_code=404, detail=f"User: '{current_user.username}' does not exists")
  db_article = crud.get_article_by_title(db, title)
  if db_article is None:
    raise HTTPException(status_code=404, detail=f"Article: '{title}' does not exists")
  article = schemas.ArticleBase(title=title, content=content, username=current_user.username)
  updated_article = crud.edit_article(db, article=article, user_id=db_user.id, article_id=db_article.id)
  if not updated_article:
    raise HTTPException(status_code=403, detail=f"You can not edit article: '{title}'")
  return updated_article

@router.delete("/delete")
def delete_article(
  title: str,
  db: Session = Depends(get_db),
  current_user: schemas.UserBase = Depends(get_current_user)
  ):
  db_article = crud.get_article_by_title(db, title)
  if db_article is None:
    raise HTTPException(status_code=404, detail=f"Article: '{title}' does not exists")
  del_article = crud.delete_article(db, article_id=db_article.id, user_id=current_user.id)
  if not del_article:
    raise HTTPException(status_code=403, detail=f"You can not delete article: '{title}'")
  return {f"Article: '{title}' has been removed"}
