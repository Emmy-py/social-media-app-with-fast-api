from time import time

from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()







# only use when runing running raw queries with psycopg2, not needed when using sqlalchemy orm
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='INPUT PASS', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
        
#         print("Database connection was successful")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)




#remove comments when using raw queries with psycopg2, not needed when using sqlalchemy orm

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#             if p["id"] == id:
#                 return i
            


@app.get("/")
async def root():
    return {"message": "Hello emmy World"}


# get post by id

# @app.get("/post/{id}")
# async def get_post(id: int, response: Response):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))    
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
#     return {"post" : post}

@app.get("/post/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    return post



# get posts

# @app.get("/post")
# async def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"message" : posts}


@app.get("/post", response_model=list[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


# create post

# @app.post("/create-post", status_code=status.HTTP_201_CREATED)
# async def create_post(post: Post):
#     cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


@app.post("/create-post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#delete post

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id:int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     Post = cursor.fetchone()
#     conn.commit()
#     if not Post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post    

# @app.put("/posts/{id}")
# async def update_post(id:int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#                    (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()

#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    
#     return {"data": updated_post } 


@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(id:int, Updated_post:schemas.PostCreate, 
                      db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the {id} was not found")
    post.update(Updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post.first() 
    

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hashed_password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user