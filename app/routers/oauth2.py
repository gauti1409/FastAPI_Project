from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from main_files import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy. orm import Session
import config

settings = config.settings

# This is going to be URL of the login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sqlalchemy_users/login")


"""Requirements that needs to be given for creating a Token:
1. SECRET KEY
2. Algorithm we are going to use
3. Expiration time for the token."""

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """This function is going to have the payload. So whatever data we want to encode into the token, we have to provide that. 
       We will pass a variable called data, which is of type dictionary. 
       Remember, the data in the payload is the one which we decide to put in. And we can put anything in the payload as per the requirement.

       Output: This function is going to return the JSON WEB TOKEN that is comprised of HEADER, PAYLOAD and SECRET_KEY. """

    # Copying the data to other variable so that the original data remains intact
    to_encode = data.copy()

    # Setting up the expiration time for the user to be logged in
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adding the expiration time property into the payload so as to have all of the data encoded into the JWT.
    to_encode.update({"exp": expire})

    # The method to create the JSON WEB TOKEN for the User
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Parameters: We are going to pass in the token, which is going to be string. And we are also going to pass in the specific
    credential exception. So, we are going to pass in what our exception should be if the credentials don't match, or there's some issue
    with the token. So, we will just store this in the variable called credentials_exception. 
    """

    try:

        # Decoding the JSON WEB TOKEN to get the fields from the Payload and save it into the variable payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Get the specific fields we require from the payload
        id = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception

        # Validating that the id matches with the schema - tokendata. See it in schemas.py
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """ We will pass this function as a dependency into any one of our path operations. And when we do that, what it's going to do is : 
    Take the token from the request automatically .Then it's going to verify that the token is correct by calling the verify access token.
    Once verified, it's going to extract the id for us. 
    And then if we want to, we can have it automatically fetch the user from the database and then add it as a parameter into our 
    path operation function.  

    Idea: The idea behind this function is that once the verify access token returns the token data, which is the ID, the get_current_user
    function should actually fetch the user from the database. And so that way we can attach the user to any path operation and then we can 
    perform any necessary logic. 
    """

    # Defining credentials exception for when the credentials are wrong or there is some issue with the JSOM WEB TOKENS
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
