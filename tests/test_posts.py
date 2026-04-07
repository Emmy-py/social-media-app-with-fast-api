
from app import schemas
import pytest

from tests.conftest import test_posts

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        # Extract the nested "Post" dict and merge with votes if needed
        return schemas.PostResponse(**post["Post"])
    
    posts_map = map(validate, res.json())
    posts = list(posts_map)
    
    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_authorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_authorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test__get__post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/99999")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post_out = schemas.PostOut(**res.json())  # validate against PostOut
    assert res.status_code == 200
    assert post_out.Post.id == test_posts[0].id
    assert post_out.Post.title == test_posts[0].title
    assert post_out.Post.content == test_posts[0].content
    assert post_out.Post.owner_id == test_posts[0].owner_id


@pytest.mark.parametrize("title, content, published", [
    ("New Post 1", "Content for new post 1", True),
    ("New Post 2", "Content for new post 2", False),
    ("New Post 3", "Content for new post 3", True)
])

def test_create_post(authorized_client, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "New Post", "content": "Content for new post"})
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert post.title == "New Post"
    assert post.content == "Content for new post"
    assert post.published is True


def test_unauthorized_user_get_create_posts(client, test_posts, test_user):
    res = client.post("/posts/", json={"title": "Unauthorized Post", "content": "Should not be created"}    )
    assert res.status_code == 401

def test_unauthorized_user_get_delete_posts(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_user_get_delete_posts_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_user_get_delete_posts_not_found(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/99999")
    assert res.status_code == 404


def test_user_get_delete_posts_forbidden(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json={"title": "Updated Title", "content": "Updated Content", "published": False})
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert post.title == "Updated Title"
    assert post.content == "Updated Content"
    assert post.published is False


def test_update_other_user_posts(authorized_client, test_user, test_user2, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json={"title": "Updated Title", "content": "Updated Content", "published": False})

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data= { 
        "title": "Updated Title", 
        "content": "Updated Content", 
        "published": False}
    
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401



def test_user_get_update_posts_not_found(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/99999", json={"title": "Updated Title", "content": "Updated Content", "published": False})
    assert res.status_code == 404