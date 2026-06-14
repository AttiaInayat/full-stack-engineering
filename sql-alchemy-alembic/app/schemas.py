from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str 

class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int