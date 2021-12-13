from os import stat
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from starlette.status import HTTP_202_ACCEPTED
from .. import models, schemas, utils
from ..database import  get_db
from typing import List


router = APIRouter(
    prefix= "/users",
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    ## hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    # if new_user == None:
    #     raise HTTPException(HTTP_208_ALREADY_REPORTED, f"user with the email {user.email} already exists!")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"user with id {id} not found!")

    return user


@router.get("/", response_model=List[schemas.UserOutput])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users



@router.post("/login", status_code= HTTP_202_ACCEPTED)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user_query = db.query(models.Users).filter(models.Users.email == user.email).first()
    if not user_query:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"user with email {user.email} not found!")
    hashed_password = utils.verify_password(user.password, user_query.password)
    

    if not hashed_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"password mismatched!")

    
    return user_query.id