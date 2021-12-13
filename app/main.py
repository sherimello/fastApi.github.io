from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.types import OptionalInt
from random import randrange
import psycopg2
from sqlalchemy import schema
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
import time
from starlette.status import HTTP_208_ALREADY_REPORTED, HTTP_404_NOT_FOUND
from . import models
from .database import engine, get_db
from .routers import user, post, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sqlalchemy")
def test_sqlalchemy(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}




while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi',
        user = 'postgres', password = '5spaces', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful!")
        break
    except Exception as error:
        print("Connection failed!")
        print("Error: ", error)
        time.sleep(2)




app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return "hello"






   


