from fastapi.testclient import TestClient
from app.main import app
from app import database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Config import settings
from app import models
import pytest


    

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testingsessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) 
Base = declarative_base()


@pytest.fixture(scope="function")
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = testingsessionlocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)