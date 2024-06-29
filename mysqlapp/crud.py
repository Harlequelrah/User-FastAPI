
from sqlalchemy.sql import func
from fastapi import  HTTPException,status,Depends
from typing import List
from . import models,schemas
from .database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session




def get_count_users(db:Session):
    return db.query(func.count(models.User.id)).scalar()



def is_email_unique(db,email: str)->bool:
    user=db.query(models.User).filter(models.User.email == email).first()
    if user:return True
    else:return False



def create_user(user:schemas.UserCreate,db:Session):
    if  not is_email_unique(db,user.email):
        db_user=models.User(
            username=user.username,
            email=user.email,
            databasename=user.databasename,
            password=models.User().set_password(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=400, detail="Cet email existe déja")







def get_user_by_email(email:str,db:Session):
    db_user=db.query(models.User).filter(models.User.email==email).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user

def get_user(id:int,db:Session):
    db_user=db.query(models.User).filter(models.User.id==id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user






def get_users(db:Session,skip:int=0,limit:int=None):
    limit=get_count_users(db)
    return db.query(models.User).offset(skip).limit(limit).all()

def get_users_by_database(databasename:str,db:Session,skip:int=0,limit:int=None):
    limit=db.query(func.count((models.User.id))).filter(models.User.databasename==databasename).scalar()
    return db.query(models.User).filter(models.User.databasename==databasename).offset(skip).limit(limit).all()

def delete_user(id: int, db: Session):
    db_user = get_user(id, db)
    if db_user is None:
        raise HTTPException(status_code=404)

    try:
        db.delete(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l 'utilisateur: {str(e)}")

    return db_user





def update_user(id:int,user:schemas.UserUpdate,db:Session):
    db_user=get_user(id,db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if user.username is not None and user.username != "string":
            db_user.username=user.username
        if user.email is not None and user.email!="string":
            db_user.email=user.email
        if user.databasename is not None and user.databasename!="string":
            db_user.databasename=user.databasename
        if user.password is not None and user.password!="string":
            db_user.password=models.User().set_password(user.password)
        db.commit()
        db.refresh(db_user)
        return db_user
