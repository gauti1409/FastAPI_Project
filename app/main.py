from fastapi import FastAPI
from app.main_files import database, models
from routers import post, users, post_orm, users_orm, auth, vote
import config
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


settings = config.settings
engine = database.engine


models.Base.metadata.create_all(bind=engine)


# Creating an instance of FastAPI
app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(post_orm.router)
app.include_router(users_orm.router)
app.include_router(vote.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
