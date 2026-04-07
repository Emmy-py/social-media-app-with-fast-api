import pytest
from app import models
 


@pytest.fixture
def test_vote(test_user, test_posts, session):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    return new_vote


def test_vote_on_post(authorized_client, test_posts, test_user):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts, test_user):
    post_id = test_posts[0].id

    # First vote
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert res.status_code == 201

    # Second vote should fail with 409
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert res.status_code == 409
    assert res.json()["detail"] == "Already voted on this post"


def test_remove_vote(authorized_client, test_posts, test_user):
    post_id = test_posts[0].id

    # First, add a vote
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert res.status_code == 201

    # Now, remove the vote
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})
    assert res.status_code == 204


def test_remove_nonexistent_vote(authorized_client, test_posts, test_user):
    post_id = test_posts[0].id

    # Ensure no vote exists
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})
    assert res.status_code == 404
    assert res.json()["detail"] == "Vote does not exist"

def test_vote_on_nonexistent_post(authorized_client, test_user):
    res = authorized_client.post("/vote/", json={"post_id": 99999, "dir": 1})
    assert res.status_code == 404
    assert res.json()["detail"] == "Post with id 99999 does not exist"


def test_unauthorized_vote(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401