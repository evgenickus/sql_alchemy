from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import database
from . import schemas
from . import crud
from .routers import users, articles

app = FastAPI()

def get_db():
  db = database.SessionLocal()
  try:
    yield db
  finally:
    db.close

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])


