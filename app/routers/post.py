from typing import Optional, List

from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor

from app import oauth2
from .. import models, schemas
from ..database import get_db



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


#remove comments when using raw queries with psycopg2, not needed when using sqlalchemy orm

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#             if p["id"] == id:
#                 return i
            



# get post by id

# @router.get("/{id}")
# async def get_post(id: int, response: Response):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))    
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
#     return {"post" : post}

from sqlalchemy import func

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db)):
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")

    post, votes = result
    return {"Post": post, "votes": votes}


# get posts

# @router.get("/post")
# async def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"message" : posts}

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    Limit: int = 10,
    skip: int = 0,
    search: str = ""
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(Limit)
        .offset(skip)
        .all()
    )
    return [{"Post": post, "votes": votes} for post, votes in results]



# create post

# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_post(post: Post):
#     cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#delete post

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id:int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     Post = cursor.fetchone()
#     conn.commit()
#     if not Post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post    

# @router.put("/{id}")
# async def update_post(id:int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#                    (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()

#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the {id} was not found")
    
#     return {"data": updated_post } 


@router.put("/{id}", response_model=schemas.PostResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_post(id:int, Updated_post:schemas.PostCreate, 
                      db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the {id} was not found")
    post.update(Updated_post.dict(), synchronize_session=False)

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db.commit()
    return  post.first() 

