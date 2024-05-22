from .. import database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

def get_db():
  db = database.SessionLocal()
  try:
    yield db
  finally:
    db.close

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
