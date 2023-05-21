from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schema,models,database
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .Config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verification_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schema.token_data(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_token_user(token:str = Depends(OAuth2PasswordBearer(tokenUrl="login")),db : Session = 
                                       Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          
                                          detail="could not validate credentials",
                                          headers={"WWW-Athenticate":"Bearer"})
    token =  verification_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
