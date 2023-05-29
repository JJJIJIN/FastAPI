from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title : str
    content : str
    publisher : bool = True

class response_user(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True


class response_post(BaseModel):
    title : str
    content : str
    publisher : bool 
    owner_id : int
    owner : response_user
    class Config:
        orm_mode = True

class Post_vote(BaseModel):
    Post : response_post
    votes : int
    class Config:
        orm_mode = True

        
class user(BaseModel):
    email : EmailStr
    password : str


    
class Userlogin(BaseModel):
    email : EmailStr
    password : str

class token(BaseModel):
    access_token : str
    token_type : str

class token_data(BaseModel):
    id : Optional[str] = None

class vote(BaseModel):
    post_id : int
    dir : conint(le = 1)


