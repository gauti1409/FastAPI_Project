from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.main_files import schemas, database, utils


get_db = database.get_db
conn = database.conn
cursor = database.cursor

# Making a router object and replace the @app command with @router command
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

"""--------------------Functions and routes related to traditional SQL Methods-------------------------"""


# Creating a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_posts(user: schemas.UserCreate):

    # hash the password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    # These below two commands are staged changes. We are staging it and we can see the result of the stage.
    cursor.execute(f"""INSERT into user_sql(email, password) VALUES (%s, %s) RETURNING * """,
                   (user.email, user.password))

    new_user = cursor.fetchone()

    # But we will have to commit to DB to actually finalize those changes.
    conn.commit()

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int):

    cursor.execute(
        """SELECT * from user_sql where id = %s""", (str(id),))

    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id:{id} does not exist. ")
    return user
