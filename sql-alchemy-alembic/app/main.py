from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models,schemas,crud
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app= FastAPI()


def get_db():
    db= SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post('/users')
def create_user(db: Session= Depends(get_db), user: schemas.UserCreate ):
    return crud.create_user(db,user)

@app.get('/users')
def get_users(db: Session= Depends(get_db) ):
    return crud.get_users(db)

@app.post('/tasks')
def create_task(db: Session= Depends(get_db), task: schemas.TaskCreate ):
    return crud.create_task(db,task)

@app.get('/tasks')
def get_task(db: Session= Depends(get_db) ):
    return crud.get_tasks(db)