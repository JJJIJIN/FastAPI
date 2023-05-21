from fastapi import FastAPI,status,HTTPException,Response,Depends
from .database import engine
from app import models
from . routers import posts,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware




#models.Base.metadata.create_all(bind = engine)

app=FastAPI()

origins = ["https://www.google.com"]

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def something():
    return {"message":"hello world"}


 









