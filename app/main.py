from time import time

from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends


models.Base.metadata.create_all(bind=engine)

app = FastAPI()





class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', 
                                user='postgres', password='#Pius2020#', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)




my_posts = [{"id":1,
             "title":"first post",
             "content":"i love coding"}, 
             {"id":2,
             "title":"second post",
             "content":"ilove system design"}, 
             ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_post_index(id):
    for i,p in enumerate(my_posts):
            if p["id"] == id:
                return i
            


@app.get("/")
async def root():
    return {"message": "Hello emmy World"}


@app.get("/sqlachemy")
def test_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {'data': post}


@app.get("/post/{id}")
async def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))    
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    return {"post" : post}

# @app.get("/post")
# async def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"message" : posts}


@app.get("/post")
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {'data': post}



@app.post("/create-post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    Post = cursor.fetchone()
    conn.commit()
    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    
    return {"data": updated_post } 
