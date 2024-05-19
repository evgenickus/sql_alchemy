from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
  username: str
  email: EmailStr

class UserCreate(UserBase):
  password: str

class ArticleBase(BaseModel):
  title: str
  content: str
  username: str

class ArticleCreate(BaseModel):
  title: str
  content: str
  user_id: int
