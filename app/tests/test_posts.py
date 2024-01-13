from ..main_files import schemas
import pytest


def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get("/sqlalchemy_posts/")
    # print(res.json())

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_post)
    assert res.status_code == 200
    # assert posts_list[0].Post.id == test_post[0].id


def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get("/sqlalchemy_posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_post):
    res = client.get(f"/sqlalchemy_posts/{test_post[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/sqlalchemy_posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/sqlalchemy_posts/{test_post[0].id}")
    # print(res.json())
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_post[0].id
    assert post.Post.content == test_post[0].content
    assert post.Post.title == test_post[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("awesome new title 2", "awesome new content 2", False),
    ("awesome new title 3", "awesome new content 3", True)

])
def test_create_post(authorized_client, test_user, test_post, title, content, published):
    res = authorized_client.post(
        "/sqlalchemy_posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_post):
    res = authorized_client.post(
        "/sqlalchemy_posts/", json={"title": "arb title", "content": "content arb"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arb title"
    assert created_post.content == "content arb"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_posts(client, test_post):
    res = client.post(
        "/sqlalchemy_posts/", json={"title": "arb title", "content": "content arb"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_post):
    res = client.delete(
        f"/sqlalchemy_posts/{test_post[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_post):
    res = authorized_client.delete(
        f"/sqlalchemy_posts/{test_post[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete(
        f"/sqlalchemy_posts/800000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_post):
    res = authorized_client.delete(
        f"/sqlalchemy_posts/{test_post[2].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_post):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_post[0].id
    }
    res = authorized_client.put(
        f"/sqlalchemy_posts/{test_post[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_post, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_post[2].id
    }
    res = authorized_client.put(
        f"/sqlalchemy_posts/{test_post[2].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_post):
    res = client.put(
        f"/sqlalchemy_posts/{test_post[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_post):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_post[2].id
    }
    res = authorized_client.put(
        f"/sqlalchemy_posts/800000", json=data)
    assert res.status_code == 404
