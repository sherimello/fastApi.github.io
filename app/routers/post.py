from app.cursor import get_cursor
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false, null
from .. import models, schemas, utils, oauth2
from ..database import  get_db
from typing import List

import app


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user:schemas.UserOutput = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()

    print(user.id)
    return posts




@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db), user:schemas.UserOutput = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()


    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id {id} not found!")
    
    return post




@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user:schemas.UserOutput = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post wiht id {id} not found!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return "post deleted!"



@router.post("/", response_model=schemas.Post, include_in_schema=False, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), user:schemas.UserOutput = Depends(oauth2.get_current_user)):
    
    print(user.email)

    if post.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"invalid user id encountered!")


    new_post = models.Post(**post.dict())
    db.add(new_post)
        
    db.commit()
    db.refresh(new_post)
    return new_post




@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), user:schemas.UserOutput = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id {id} not found!")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()




@router.get("/post/count")
def get_post_count(db: Session = Depends(get_db), user:schemas.UserOutput = Depends(oauth2.get_current_user)):
    # r = db.query(models.Post).count()
    # cur = cursor.get_cursor()
    # cur.execute("""SELECT COUNT(*) FROM posts""")
    # rows = cur.fetchone()

    return db.query(models.Post).count()