from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from .dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.ArticleBase])
def read_articles(db: Session = Depends(get_db)):
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
def add_article(article_data: schemas.ArticleBase, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_username(db, article_data.username)
  if db_user is None:
    raise HTTPException(status_code=404, detail=f"User: '{article_data.username}' does not exists")
  article = schemas.ArticleCreate(title=article_data.title, content=article_data.content, user_id=db_user.id)
  return crud.create_article(db, article, article_data.username)

@router.patch("/", response_model=schemas.ArticleBase)
def edit_article(title: str, article_data: schemas.ArticleBase, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_username(db, article_data.username)
  if db_user is None:
    raise HTTPException(status_code=404, detail=f"User: '{article_data.username}' does not exists")
  db_article = crud.get_article_by_title(db, title)
  if db_article is None:
    raise HTTPException(status_code=404, detail=f"Article: '{title}' does not exists")
  updated_article = crud.edit_article(
    db, article=article_data, user_id=db_user.id, article_id=db_article.id
  )
  return updated_article

@router.delete("/delete")
def delete_article(title: str, db: Session = Depends(get_db)):
  db_article = crud.get_article_by_title(db, title)
  if db_article is None:
    raise HTTPException(status_code=404, detail=f"Article: '{title}' does not exists")
  crud.delete_article(db, article_id=db_article.id)
  return {f"Article: '{title}' has been removed"}
