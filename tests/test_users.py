from app import schema
import pytest
from jose import jwt
from app.Config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == "fucking world!!!"


def test_create_users(client):
    res = client.post("/user/",json={"email":"johan@gmail.com",
                                    "password":"password123"})
    new_user = schema.response_user(**res.json())
    assert new_user.email == "johan@gmail.com"
    assert res.status_code ==201 

def test_login(client,test_user):
    res = client.post("/login",data={"username":test_user["email"],"password":"password123"})
    login_user = schema.token(**res.json())
    payload = jwt.decode(login_user.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id  = payload.get("user_id")
    assert id == test_user["id"]
    assert login_user.token_type == "Bearer"
    print(res.json())
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code