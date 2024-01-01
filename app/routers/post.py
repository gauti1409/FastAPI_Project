from typing import List
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from main_files import schemas, database

get_db = database.get_db
conn = database.conn
cursor = database.cursor


# Making a router object and replace the @app command with @router command
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

"""--------------------Functions and routes related to traditional SQL Methods-------------------------"""


# Getting all posts
@router.get("/", response_model=List[schemas.Post])
def get_posts():

    # Passing the SQL Statement
    cursor.execute("""SELECT * from social_media_posts""")
    posts = cursor.fetchall()
    return posts


# Creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate):
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    # These below two commands are staged changes. We are staging it and we can see the result of the stage.
    cursor.execute(f"""INSERT into social_media_posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))

    new_post = cursor.fetchone()

    # But we will have to commit to DB to actually finalize those changes.
    conn.commit()

    return new_post


# Getting an individual post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int):

    # post = find_post(id)

    cursor.execute(
        """SELECT * from social_media_posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found.")

    return post


# To delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # index = find_index_post(id)

    cursor.execute(
        """DELETE from social_media_posts WHERE id = %s RETURNING *""", (str(id),))

    deleted_post = cursor.fetchone()

    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist.")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# To update a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate):

    # index = find_index_post(id)

    cursor.execute("""UPDATE social_media_posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist.")

    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    return updated_post
