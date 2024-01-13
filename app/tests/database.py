from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..main import app
from ..config import settings
from ..main_files.database import get_db, Base

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
