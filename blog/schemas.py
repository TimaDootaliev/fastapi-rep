from typing import List, Optional
from pydantic import BaseModel


class BaseBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class Blog(BaseBlog):
    class Config:
        orm_mode = True



class User(BaseModel):
    name: str
    email: str
    password: str

    

class ShowUser(BaseModel):
    name: str
    email: str
    posts: List[Blog] = []

    class Config:
        orm_mode = True
    

class ShowBlog(BaseModel):
    title: str
    body: str
    author: ShowUser
    
    class Config:
        orm_mode = True