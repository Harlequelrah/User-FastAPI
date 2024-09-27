
from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    databasename:str

class UserUpdate(BaseModel):
    username:Optional[str]=None
    email: Optional[str]=None
    password: Optional[str]=None
    databasename: Optional[str]=None

class User(UserCreate):
    id:int
    class config:
        from_attributes = True

class AccessToken(BaseModel):
    access_token: str
    token_type: str
class RefreshToken(BaseModel):
    refresh_token:str
    token_type:str
class Tokens(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken
