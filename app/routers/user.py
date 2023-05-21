from .. import models,utils,schema
from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List

router  = APIRouter(prefix="/user",tags=['Users'])


@router.get("/",response_model=List[schema.response_user])
def get_user(db : Session = Depends(get_db)):
    user_db = db.query(models.User).all()
    return user_db

@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schema.response_user)
def new_users(post : schema.user, db : Session = Depends(get_db)):
    hashed_password = utils.pass_hash(post.password)
    post.password = hashed_password
    new_user = models.User(**post.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{id}",response_model=schema.response_user)
def update_users(id:int,user:schema.user,db : Session = Depends(get_db)):
    updated_user = db.query(models.User).filter(models.User.id == id)
    if not updated_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                             detail= f"the post with {id} is not found")
    
    updated_user.update(user.dict(),synchronize_session=False)
    db.commit()
    return updated_user.first()