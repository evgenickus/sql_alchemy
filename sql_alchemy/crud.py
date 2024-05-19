from sqlalchemy.orm import Session
from sqlalchemy import select, update
from . import models
from . import schemas


# users
def get_users(db: Session):
  users = select(models.User)
  # print("------------",db.scalar(users).username)
  return db.scalars(users).all()

def get_user_by_username(db: Session, username: str):
  user = select(models.User).where(models.User.username == username)
  return db.scalar(user)


def get_user_by_email(db: Session, email: str):
  user = select(models.User).where(models.User.email == email)
  return db.scalar(user)

def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = user.password + "hashedpassword"
  new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
  db.add(new_user)
  db.commit()
  return schemas.UserBase(username=new_user.username, email=new_user.email)

#articles
def get_articles(db: Session):
  articles = select(models.Article.content, models.Article.title, models.User.username).join(models.User)
  return db.execute(articles).all()

def get_article_by_title(db: Session, title: str):
  article = select(models.Article).where(models.Article.title == title)
  return db.scalar(article)

def create_article(db: Session, article: schemas.ArticleCreate, username: str):
  new_article = models.Article(title=article.title, content=article.content, user_id=article.user_id)
  db.add(new_article)
  db.commit()
  return schemas.ArticleBase(title=new_article.title, content=article.content, username=username)

def edit_article(db: Session, article: schemas.ArticleBase, user_id: int, article_id: int):
  stmt = update(models.Article).where(
    models.Article.id == article_id).values(
      title=article.title, content=article.content, user_id=user_id)
  db.execute(stmt)
  db.commit()
  updated_article = schemas.ArticleBase(title=article.title, content=article.content, username=article.username)
  return updated_article



