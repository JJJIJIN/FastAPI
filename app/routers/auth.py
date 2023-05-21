from fastapi import status,HTTPException,Response,Depends,APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schema,utils,oauth2


router  = APIRouter(tags = ['Authentication'])

@router.post("/login",response_model=schema.token)
def login(credentials :OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credential")
    
    if not utils.verification(credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credential")
    
    access_token = oauth2.access_token(data = {"user_id":user.id})
    
    return {"access_token" : access_token , "token_type":"Bearer"}