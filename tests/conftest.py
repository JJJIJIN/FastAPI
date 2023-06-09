import pytest
from app import models
from fastapi.testclient import TestClient
from app.main import app
from app import database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Config import settings
from app import models
import pytest
from app.oauth2 import access_token


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

@pytest.fixture
def test_user(client):
    user_data={"email":"lifeofram@gmail.com",
                                    "password":"password123"}
    res = client.post("/user/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    # new_user['email'] = user_data["email"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data={"email":"jijinjj@gmail.com",
                                    "password":"password123"}
    res = client.post("/user/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    # new_user['email'] = user_data["email"]
    return new_user

@pytest.fixture
def token(test_user):
    return access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers =  {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session,test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4rd title",
        "content": "4rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts