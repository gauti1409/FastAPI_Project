from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from main_files import schemas, database, utils, models


get_db = database.get_db
conn = database.conn
cursor = database.cursor

# Making a router object and replace the @app command with @router command
router = APIRouter(
    prefix="/sqlalchemy_users",
    tags=['SQLALCHEMY_Users']
)


"""--------------------Writing tests and functions for ORM--------------------------------"""

# Creating the user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id:{id} does not exist. ")
    return user
