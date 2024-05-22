from fastapi import FastAPI
from . import database
from .routers import users, articles, auth

app = FastAPI()

def get_db():
  db = database.SessionLocal()
  try:
    yield db
  finally:
    db.close

app.include_router(auth.router, prefix="/token", tags=["authentincate"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])


