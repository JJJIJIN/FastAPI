from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import null,text
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publisher = Column(Boolean, server_default='TRUE',nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("Users.id",ondelete = "CASCADE"),nullable = False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True,nullable= False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))

class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True)