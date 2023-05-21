from .. import models,schema
from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from typing import List,Optional
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import oauth2
from sqlalchemy import func


router  = APIRouter(
    prefix="/sqlachemy",tags = ['Posts']
)


@router.get("/",response_model=List[schema.Post_vote])
def test_posts(db : Session = Depends(get_db),
               current_user :int = Depends(oauth2.get_token_user),
               limit:int = 10,skip = 2,search:Optional[str] = ""):
    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
    return result

@router.post("/",status_code = status.HTTP_201_CREATED, response_model=schema.response_post)
def new_posts(post : schema.Post, db : Session = Depends(get_db),
              current_user :int = Depends(oauth2.get_token_user)):
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schema.Post_vote)
def get_single_post(id: int , db : Session = Depends(get_db),
                    current_user :int = Depends(oauth2.get_token_user)):
    #single_post = db.query(models.Post).filter(models.Post.id == id).first()
    single_post = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                             detail= f"the post with {id} is not found")
    # if single_post.first().id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
    #                          detail= "not authorized to perform requested action")
    return single_post


@router.delete("/{id}")
def delete_single_post(id: int , db : Session = Depends(get_db),
                       current_user :int = Depends(oauth2.get_token_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                             detail= f"the post with {id} is not found")
    if delete_post.first().id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                             detail= "not authorized to perform requested action")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.response_post)
def get_single_post(id: int ,posts :schema.Post , db : Session = Depends(get_db),
                    current_user :int = Depends(oauth2.get_token_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                             detail= f"the post with {id} is not found")
    if updated_post.first().id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                             detail= "not authorized to perform requested action")
    
    updated_post.update(posts.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()