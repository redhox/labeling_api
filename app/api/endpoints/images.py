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
#from jose import JWTError, jwt
import jwt
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
from bson import json_util
from app.detection import image_detection
from fastapi.responses import Response
from app.api.endpoints.users import get_current_user,SystemUser
router = APIRouter()

class ImageData(BaseModel):
    filename: str
    filedir: str
    path: str
    regions: list
    uuid_machine: str

class pathData(BaseModel):
    path: str 
class Image_label(BaseModel):
    uuid: str 
    projet_name: str   
    download: bool

@router.put("/post_resultat") 
async def post_resultat(data: ImageData,current_user: SystemUser = Depends(get_current_user)): 
    print('post_resultat') 
    print(data) 
    image_data = MongoAccess().phind_path(data.path)
    print('imagedata',image_data)
    if image_data is None:
        image = MongoAccess().incert_image(data.dict())
        return {"status": "success", "action": "created"}
    else: 
        image = MongoAccess().change_label(image_data['_id'], data.regions)
        return {"status": "success", "action": "updated"}  


@router.post("/image_save")
async def image_save_on_bucket(file: UploadFile = File(...),path: str = Form(...),model: str = Form(...),current_user: SystemUser = Depends(get_current_user)):   
    try:
        contents = await file.read() # Lecture ducontenu du fichier
        print('image_save ',file.filename)
        if not os.path.exists('image_temp'):
            os.makedirs('image_temp')
        with open(f'image_temp/{file.filename}', 'wb') as buffer:  # Ouverture du fichier en mode écriture binaire
            buffer.write(contents)  # Écriture du contenu dans le fichier
        print('image_save ping1')

        manager = MinioBucketManager()  # Create an instance
        manager.upload_file(f'image_temp/{file.filename}', f'raw_image/{path}')
        print('image_save ping2')
        label_image=image_detection(f'image_temp/{file.filename}',model)

        # try:
        #     label_image=image_detection(f'image_temp/{file.filename}',model)
        # except:
        #     label_image={'regions': []}
        print('label image',label_image)
        os.remove(f'image_temp/{file.filename}')
        return label_image  # Retourne le nom du fichier téléchargé

    except Exception as e:
        return {"error": str(e)}  # Gestion des exceptions


@router.post("/image_search")
async def image_search(path: str = Form(...),current_user: SystemUser = Depends(get_current_user)): 
    print("image_search")
    print('path=', path)

    image_data = MongoAccess().phind_path(path)
    print('image data', image_data) 
    if image_data is None:
        return Response(status_code=404)  # Use 404 instead of 401 for not found
        # Convert ObjectId to string
    if '_id' in image_data:
        image_data['_id'] = str(image_data['_id'])

    return JSONResponse(content=image_data, status_code=200)

 
@router.post("/labels")
async def image_labels(data: Image_label,current_user: SystemUser = Depends(get_current_user)): 
    data_label = MongoAccess().phind_dir_uuid(data.projet_name,data.uuid) 
    if data.download == False:
        print(data_label)
        if data_label == []:
            data_label={"message":False}
        else :
            data_label={"message":True}
    print("data label dl=",data_label)
        
    return  json_util.dumps(data_label)