from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from . import schemas, database, models




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="posts")

SECRET_KEY = "396de43fc7a50844e08fc4d98799623871b81d2d097d90f2e163472e17d77272"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token= token, key=SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception


    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, f"Couldn't verify credentials!", headers=
    {"WWW-Authentication": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user