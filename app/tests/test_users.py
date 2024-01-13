from ..main_files import schemas
# from .database import client, session
from ..config import settings
from jose import jwt
import pytest


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert (res.json().get('message')) == "Hello World !!"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/sqlalchemy_users/", json={"email": "dhruv123@gmail.com", "password": "dhruv"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "dhruv123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/sqlalchemy_users/login", data={"username": test_user["email"], "password": test_user["password"]})

    # print(res.json())
    login_res = schemas.Token(**res.json())

    # Decoding the JSON WEB TOKEN to get the fields from the Payload and save it into the variable payload
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])

    # Get the specific fields we require from the payload
    id = payload.get("user_id")

    assert id == test_user["id"]

    assert login_res.token_type == "bearer"

    assert res.status_code == 200


@pytest.mark.parametrize('email, password, status_code',
                         [('wrong@email.com', '1werr', 403),
                          ('dgf@gmail.com', 'dfdd', 403),
                          (None, 'dfdd', 422),
                          ('dgf@gmail.com', None, 422)])
def test_incorrect_login(test_user, client, email, password, status_code):

    res = client.post("/sqlalchemy_users/login", data={"username": email,
                                                       "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"
