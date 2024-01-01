from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session  # Importing the databse session
from main_files import schemas, database, utils, models
from . import oauth2


get_db = database.get_db
conn = database.conn
cursor = database.cursor

router = APIRouter(tags=["Authentication"])


@router.post("/sqlalchemy_users/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2PasswordRequestForm returns the user's credentials in the fields naming Username and Password.
    {"username":"", "password":} """

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Logic for hashing the password given by the user and then comparing it with stored in the database to see if they are equal
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Create a token
    # return a token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
