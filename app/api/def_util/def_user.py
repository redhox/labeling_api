from fastapi_login import LoginManager
from datetime import datetime, timedelta
from app.models.users_model import *
from pydantic_settings import BaseSettings
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.connector.connectorBDD_user import PostgresAccess
from fastapi import APIRouter, Depends, HTTPException,status
# from app.crud.users_crud import UserCRUD
from app.models.users_model import *
from bson import ObjectId
from app.connector.connectorBDD_user import PostgresAccess
from typing import List
import bcrypt
from datetime import datetime, timedelta
import os
#from jose import JWTError, jwt
from app.api.def_util.def_user import *
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel ,EmailStr
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from flask import jsonify
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic_settings import BaseSettings
import pytest
from unittest.mock import Mock, patch
# Assurez-vous de l'import correct si vous utilisez pyjwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

TOKEN_URL = "/users/token"
manager = LoginManager(SECRET_KEY, TOKEN_URL)
@manager.user_loader()
def get_user(email: str):
    user = PostgresAccess().get_user_by_email(email)
    return  user


def get_db_access():
    """
    Fournit un accès à la base de données via la classe MongoAccess.
    Cela permet une séparation claire entre la couche d'accès aux données et la logique de l'application.

    Returns:
        Instance de MongoAccess qui offre une connexion aux collections MongoDB spécifiques.
    """
    return PostgresAccess()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=99999)
    
    # Convertir `expire` en timestamp (entier)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    print('getuser')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Convertir `exp` en entier si nécessaire
        if isinstance(payload.get("exp"), datetime):
            payload["exp"] = int(payload["exp"].timestamp())

        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("get_current_user")

    # Utilisation de la méthode get_user_by_username pour récupérer l'utilisateur
    user = PostgresAccess().get_user_by_email(token_data.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user