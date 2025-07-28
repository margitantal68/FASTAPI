from sqlalchemy import Column, Integer, String
from sqlalchemy.orm  import declarative_base
from database import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class UserResponse(BaseModel):
    username: str
    email: str 

class UserRequest(BaseModel):
    username: str
    fullname: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    message: str
    username: str
    access_token: str
    access_token_type: str = "bearer"

class ResponseMessage(BaseModel):
    message: str