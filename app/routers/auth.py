from fastapi import APIRouter, Depends, routing, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schemas, models, utils, oauth2


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/", response_model=schemas.Token)
def user_login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user_query = db.query(models.Users).filter(models.Users.email == user.username).first()

    if not user_query:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"invalid credentials!")

    if not utils.verify_password(user.password, user_query.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"invalid credentials!")

    access_token = oauth2.create_access_token({"user_id": user_query.id})

    return {"access_token": access_token, "token_type": "bearer"}