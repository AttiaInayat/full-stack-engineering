from sqlalchemy import Session
from . import models


def create_user(db: Session, user):
    db_user= models.User(**user.model_dump())
    db.add(db_user) 
    db.commit()
    db.refresh(db_user)
    return db_user



def create_task(db: Session, task):
    db_task= models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task 


def get_users(db: Session):
    return db.query(models.User).all()


def get_tasks(db: Session):
    return db.query(models.Task).all()