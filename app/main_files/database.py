from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..config import settings
# import config

# settings = config.settings


# Format of a Connection String to be passed into the SQL ALCHEMY
# SQLALACHEMY_DATABSE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALACHEMY_DATABSE_URL = f"""postgresql://{
    settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"""

# CREATE AN ENGINE. IT IS RESPONSIBLE FOR SQLALCHEMY TO CONNECT TO A POSTGRES DATABASE.
engine = create_engine(SQLALACHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""Making a Postgresql DB Connection """

# Establishing a connection with Postgres Table
while True:
    try:
        conn = psycopg2.connect(
            host=f"{settings.database_hostname}",
            database=f"{settings.database_name}",
            user=f"{settings.database_username}",
            password=f"{settings.database_password}",
            cursor_factory=RealDictCursor)

        cursor = conn.cursor()

        print("Database Connection was successful !!")

        break

    except Exception as error:
        print("Connecting to database Failed !!")
        print(f"Error: {error} ")
        time.sleep(2)
