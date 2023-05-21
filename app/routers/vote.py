from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from .. import schema,models
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import oauth2

router  = APIRouter(prefix="/vote",tags=['Votes'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schema.vote,db : Session = Depends(get_db),
         current_user = Depends(oauth2.get_token_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{vote.post_id} does not exit")
    vote_query = db.query(models.Votes).filter(vote.post_id == models.Votes.post_id,
                                               current_user.id == models.Votes.user_id)
                                              
    found_vote = vote_query.first()
    

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user{current_user.id} has already voted {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote doesnt exit")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"sucessfully deleted"}
     
         
        