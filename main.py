from datetime import timedelta
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
from mysqlapp import crud, schemas, models, authenticate
from mysqlapp.database import Base, engine, get_db
from mysqlapp.schemas import Token
from mysqlapp.authenticate import authenticate_user, create_access_token
from typing import List

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}







ACCESS_TOKEN_EXPIRE_MINUTES = 30







@app.get('/get-user/{id}',response_model=schemas.User)
async def get_user(id:int,db:Session=Depends(get_db),current_user: models.User = Depends(authenticate.get_current_user)):
    return crud.get_user(id,db)

@app.get('/get-user/by-email/{email}',response_model=schemas.User)
async def get_user(email:str,db:Session=Depends(get_db),current_user: models.User = Depends(authenticate.get_current_user)):
    return crud.get_user_by_email(email,db)

@app.get('/get-users',response_model=list[schemas.User])
async def get_users(db:Session=Depends(get_db),current_user: models.User = Depends(authenticate.get_current_user)):
    return crud.get_users(db)

@app.get('/get-users/by-{databasename}',response_model=list[schemas.User])
async def get_users_by_databasename(databasename:str,db:Session=Depends(get_db)):
    return crud.get_users_by_database(databasename,db)


@app.get('/count-users')
async def count_users(db:Session=Depends(get_db),current_user: models.User = Depends(authenticate.get_current_user)):
    return crud.get_count_users(db)

@app.post('/create-user',response_model=schemas.User)
async def create_user(user:schemas.UserCreate,db:Session=Depends(get_db),current_user: models.User = Depends(authenticate.get_current_user)):
    return crud.create_user(user,db)

@app.put('/update-user/{id}',response_model=schemas.User)
def update_user(id:int,user:schemas.UserUpdate,db:Session=Depends(get_db),current_user: models.User = Depends(authenticate.get_current_user)):
    return crud.update_user(id,user,db)

@app.delete('/delete-user/{id}',response_model=schemas.User)
def delete_user(id:int,db:Session=Depends(get_db),current_user: models.User = Depends(authenticate.get_current_user)):
    return crud.delete_user(id,db)


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(authenticate.get_current_user)):
    return current_user


if __name__ == '__main__':
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
