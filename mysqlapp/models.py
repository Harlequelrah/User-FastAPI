from sqlalchemy import DECIMAL, Column, DateTime,Integer,String,Date,Enum
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
import enum
from fastapi import HTTPException,status
import bcrypt



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(256))
    email = Column(String(256), unique=True, index=True)
    databasename=Column(String(50), index=True)

    def set_password(self,password: str):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return self.password

    def check_password(self,password:str) -> bool:
        if bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8')):return True
        else:raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid  password",
        headers={"WWW-Authenticate": "Bearer"},
    )


