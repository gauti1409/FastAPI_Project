from passlib.context import CryptContext

# Telling passlib, what is the default hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


# Comparing the hash and plain password for verification
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
