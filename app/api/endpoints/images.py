from fastapi import APIRouter, Depends, HTTPException,status,UploadFile, File, Form, Body
# from app.crud.users_crud import UserCRUD
from app.models.users_model import UserCreate, UserDisplay , Usermail,Userid,UserLogin
from bson import ObjectId
from app.connector.connectorBDD_image import MongoAccess
from app.connector.connectorBucket import MinioBucketManager
from typing import List
import bcrypt
from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from flask import jsonify
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic_settings import BaseSettings
import json
router = APIRouter()

class ImageData(BaseModel):
    filename: str
    filedir: str
    path: str
    regions: list
    uuid_machine: str

@router.post("/post_resultat")
async def post_resultat(data: ImageData): 

    print(data)
    image = MongoAccess().incert_image(data.dict())
    print('bonjour')



@router.post("/image_save")
async def image_save_on_bucket(file: UploadFile = File(...),path: str = Form(...)):   
    try:
        contents = await file.read() # Lecture ducontenu du fichier
        print('path: ',path )
        print('plus',file.filename)

        with open(f'image_temp/{file.filename}', 'wb') as buffer:  # Ouverture du fichier en mode écriture binaire
            buffer.write(contents)  # Écriture du contenu dans le fichier
        manager = MinioBucketManager()  # Create an instance
        manager.upload_file(f'image_temp/{file.filename}', f'raw_image/{path}') 
        os.remove(f'image_temp/{file.filename}')
        return {"filename": file.filename}  # Retourne le nom du fichier téléchargé

    except Exception as e:
        return {"error": str(e)}  # Gestion des exceptions
    
    manager = MinioBucketManager()  # Create an instance
    manager.upload_file('/app/testapi.py', 'dossier/cool/testapi.py') 
    # image = MinioBucketManager.upload_file('/app/testapi.py', 'testapi.py')
    print('bonjour') 