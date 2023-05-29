from app import schema
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/sqlachemy/")
    def validate(post):
        return schema.response_post(**post)
    posts_map = map(validate,res.json())
    print(posts_map)

    assert len(res.json())==len(test_posts)
    assert res.status_code == 200

def test_unauthorised_user_get_all_posts(client,test_posts):
    res = client.get("/sqlachemy/")
    assert res.status_code == 401

def test_unauthorised_user_get_one_posts(client,test_posts):
    res = client.get(f"/sqlachemy/{test_posts[0].id}")
    assert res.status_code == 401

def test_unauthorised_one_posts_doesnotexit(authorized_client,test_posts):
    res = authorized_client.get(f"/sqlachemy/22")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/sqlachemy/{test_posts[0].id}")
    print(res.json())
    post = schema.Post_vote(**res.json())
    assert post.Post.owner_id == test_posts[0].id

@pytest.mark.parametrize("title,content,publisher",[
    ("awesome","who is awesome",True),
    ("hardwork","hardwork beats talent",True),
    ("talent","they are smart",True),
])
def test_create_post(authorized_client,test_posts,test_user,title,content,publisher):
    res = authorized_client.post("/sqlachemy/",json={"title":title,"content":content,"publisher":publisher})
    created_post = schema.response_post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title

def test_create_unauthorized(client,test_posts,test_user):
    res = client.post("/sqlachemy/",json={"title":"woow","content":"fuck the people"})
    assert res.status_code == 401


    
def test_delete_unauthorized(client,test_posts,test_user):
    res = client.delete(f"/sqlachemy/{test_posts[0].id}")
    assert res.status_code == 401  

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/sqlachemy/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/sqlachemy/8000000")

    assert res.status_code == 404

def test_delete_another_users_posts(authorized_client,test_posts,test_user):

    res = authorized_client.delete(
            f"/sqlachemy/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_authorised_post(authorized_client,test_posts,test_user):
    data = {
        "title":"updated posts",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res = authorized_client.put(
            f"/sqlachemy/{test_posts[0].id}",json=data)
    updated_post = schema.response_post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/sqlachemy/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/sqlachemy/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/sqlachemy/8000000", json=data)

    assert res.status_code == 404