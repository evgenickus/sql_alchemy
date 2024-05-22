from fastapi import Depends, HTTPException, status, APIRouter
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .dependencies import get_db, oauth2_scheme, OAuth2PasswordRequestForm
from .. import crud, schemas
from typing import Union
from datetime import datetime, timedelta, timezone

router = APIRouter()

SECRET_KEY = "2c4404d4c97419990d6c9f47719f50e487ef04e13f202f646460e2ccea2db1a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  # return pwd_context.verify(plain_password, hashed_password)
  if plain_password + "hashedpassword" == hashed_password:
    return True
  else:
    return False


def get_password_hash(password):
  # return pwd_context.hash(password)
  return password + "hashedpassword"
  

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
  user = crud.get_user_by_username(db, username)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt
  
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("sub")
    if user_id is None:
      raise credentials_exception
    token_data = schemas.TokenData(user_id=user_id)
  except jwt.exceptions.InvalidTokenError:
    raise credentials_exception

  user = crud.get_user_by_user_id(db, user_id=token_data.user_id)
  if user is None:
    raise credentials_exception
  print(user)
  return user

@router.post("/")
async def login_for_access_token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
  ) -> schemas.Token:
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect usename or password",
      headers={"WWW-Authenticate": "Bearer"}
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.id}, expires_delta=access_token_expires
  )
  return schemas.Token(access_token=access_token, type_token="bearer")

