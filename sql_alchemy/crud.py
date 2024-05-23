from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
from . import models
from . import schemas
from .routers.auth import get_password_hash


# users
def get_users(db: Session):
  users = select(models.User)
  return db.scalars(users).all()

def get_user_by_username(db: Session, username: str):
  user = select(models.User).where(models.User.username == username)
  return db.scalar(user)

def get_user_by_user_id(db: Session, user_id: str):
  user = select(models.User).where(models.User.id == user_id)
  return db.scalar(user)


def get_user_by_email(db: Session, email: str):
  user = select(models.User).where(models.User.email == email)
  return db.scalar(user)

def create_user(db: Session, user: schemas.UserCreate):
  # hashed_password = user.password + "hashedpassword"
  hashed_password = get_password_hash(user.password)
  new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
  db.add(new_user)
  db.commit()
  return schemas.UserBase(username=new_user.username, email=new_user.email)

#articles
def get_articles(db: Session):
  articles = select(models.Article.title, models.Article.content, models.User.username).join(models.User)
  return db.execute(articles).all()

def get_titles(db: Session):
  titles = select(models.Article.title)
  return db.execute(titles).all()

def select_article_by_user_id(db: Session, user_id: int):
  articles = select(
    models.Article.title,
    models.Article.content,
    models.User.username
    ).join(models.User).where(models.Article.user_id == user_id)
  return db.execute(articles).all()

def get_article_by_title(db: Session, title: str):
  article = select(models.Article).where(models.Article.title == title)
  return db.scalar(article)

def search_article_like_title(db: Session, title: str):
  article = select(
    models.Article.content,
    models.Article.title,
    models.User.username
  ).join(models.User).where(models.Article.title.contains(title.lower()))
  return db.execute(article).all()

# def search_article_like_title(db: Session, title: str):
#   articles_list = db.scalars(select(models.Article.title)).all()
#   lower_case = [item.lower() for item in articles_list]
  
#   article = select(
#     models.Article.content,
#     models.Article.title,
#     models.User.username
#   ).join(models.User).where(models.Article.title.contains(title.lower()))
#   return db.execute(article).all()


def create_article(db: Session, article: schemas.ArticleCreate, username: str):
  new_article = models.Article(title=article.title, content=article.content, user_id=article.user_id)
  db.add(new_article)
  db.commit()
  return schemas.ArticleBase(title=new_article.title, content=article.content, username=username)

def edit_article(db: Session, article: schemas.ArticleBase, user_id: int, article_id: int):
  db_article = select(models.Article).where(models.Article.id == article_id).where(models.Article.user_id == user_id)
  if db.scalar(db_article) is None:
    return False
  else:
    stmt = update(models.Article).where(
      models.Article.id == article_id).values(
        title=article.title, content=article.content, user_id=user_id)
    db.execute(stmt)
    db.commit()
    updated_article = schemas.ArticleBase(title=article.title, content=article.content, username=article.username)
    return updated_article

def delete_article(db: Session, article_id: int, user_id: int):
  article = select(models.Article).where(models.Article.id == article_id).where(models.Article.user_id == user_id)
  if db.scalar(article) is None:
    return False
  else:
    stmt = delete(models.Article).where(models.Article.id == article_id).where(models.Article.user_id == user_id)
    db.execute(stmt)
    db.commit()
  return True

