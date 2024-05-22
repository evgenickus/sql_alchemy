from pydantic import BaseModel, EmailStr
from typing import Union

class UserBase(BaseModel):
  username: str
  email: EmailStr

class UserCreate(UserBase):
  password: str

class UserInDB(UserBase):
  hashed_password: str

class ArticleBase(BaseModel):
  title: str
  content: str
  username: str

class ArticleCreate(BaseModel):
  title: str
  content: str
  user_id: int

class Token(BaseModel):
  access_token: str
  type_token: str

class TokenData(BaseModel):
  user_id: Union[int, None] = None 
