from time import time

from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2

from psycopg2.extras import RealDictCursor

from app.routers import auth
from . import models, schemas
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from .utils import hash
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")
async def root():
    return {"message": "Hello emmy World"}


