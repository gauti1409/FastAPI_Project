"""This is a special file that pytest uses. It allows us to define Fixtures in here. And any fixtures you define in this file will 
automatically be accessible to any of our tests within this package. So it's package specific.
So, anything within the tests package, even the subpackages will automatically have access to these fixtures. """

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..main import app
from ..config import settings
from ..main_files.database import get_db, Base
from ..routers.oauth2 import create_access_token
from ..main_files import models

import pytest

SQLALACHEMY_DATABSE_URL = f"""postgresql://{
    settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"""

# CREATE AN ENGINE. IT IS RESPONSIBLE FOR SQLALCHEMY TO CONNECT TO A POSTGRES DATABASE.
engine = create_engine(SQLALACHEMY_DATABSE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# client = TestClient(app)


@pytest.fixture()
def session():
    # Drop the tables after the tests are completed that were generated in the previous run
    Base.metadata.drop_all(bind=engine)

    # create all the tables in database before we run a test
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    # Overriding the dependency of the get_db Session with the Testing Session so as to test the API Endpoints in a different DB.
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "dhruv123@gmail.com", "password": "dhruv"}
    res = client.post("/sqlalchemy_users/", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "dhruv@gmail.com", "password": "dhruv"}
    res = client.post("/sqlalchemy_users/", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers,
                      "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_post(test_user, session, test_user2):
    posts_data = [{
        "title": "title 1",
        "content": "content 1",
        "owner_id": test_user["id"]
    },
        {
        "title": "title 2",
        "content": "content 2",
        "owner_id": test_user["id"]
    }, {
        "title": "title 3",
        "content": "content 3",
        "owner_id": test_user2["id"]
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="title 1", content="content 1", owner_id=test_user["id"]),
    #                  models.Post(title="title 1", content="content 1",
    #                              owner_id=test_user["id"])])

    session.commit()

    posts = session.query(models.Post).all()

    return posts
