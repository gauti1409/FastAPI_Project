from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Here, we can provide a list of all the environment variables that we need to set as properties on the class itself. 

    How it works: If there is no default value being assigned to the below variables, then this validation will first check my system or 
    user environment variables to see if there's something called database_password. And since we haven't provided any default ones or there is
    no environment variable with that name, it's going to throw an error as it's point is to validate all of the environment vairables 
    that we have are configured here."""

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()
