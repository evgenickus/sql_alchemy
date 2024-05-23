from .. import database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
# from sqlalchemy.orm import Session
# from .auth import get_current_user
# from .. import crud
def get_db():
  db = database.SessionLocal()
  try:
    yield db
  finally:
    db.close

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

