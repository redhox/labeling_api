from fastapi import APIRouter, Depends, HTTPException,status,UploadFile, File, Form, Body
# from app.crud.users_crud import UserCRUD
from app.models.users_model import UserCreate, UserDisplay , Usermail,Userid,UserLogin
from bson import ObjectId
from app.connector.connectorBucket import MinioBucketMLflow
from app.connector.connectorMLflow import MlflowConnect
from app.connector.connectorBDD_image import MongoAccess
from app.api.endpoints.users import get_current_user,SystemUser
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
from bson import json_util
from app.detection import image_detection
from fastapi.responses import Response
router = APIRouter()

def download_model():
    print('model to dl')
    if not os.path.exists('models'):
        os.makedirs('models')
    model_data = MongoAccess().phind_all_model()
    liste_model_actif=[]
    for run in model_data:
        liste_model_actif.append(f'{run["run_id"]}.pt')
        if not os.path.exists(f'models/{run["run_id"]}.pt'):
            MinioBucketMLflow().dl_model(f'{run["path"]}/weights/best.pt',f'models/{run["run_id"]}.pt')
    models_dir_list = os.listdir('models')
    model_to_rm = []
    for x in models_dir_list:
        if x not in liste_model_actif:
            model_to_rm.append(x)
    for model in model_to_rm:
        os.remove(f'models/{model}')




@router.post("/lists_models") 
async def lists_models(current_user: SystemUser = Depends(get_current_user)): 
    print('all_model') 
    list_model = MlflowConnect.liste_mlflow()
    return json_util.dumps(list_model)


class Modelid(BaseModel):
    id: str



@router.put("/add_model_id") 
async def lists_models(model_id: Modelid,current_user: SystemUser = Depends(get_current_user)):
    print('add_model',model_id) 
    model_id=model_id.id
    model_data = MlflowConnect.run_by_id(model_id)

    print(model_data) 
    model = MongoAccess().phind_model_id(model_id)
    print('model',model) 
    if model ==None:
        model = MongoAccess().incert_model(model_data)
    download_model()
    return {'message':'model added'}

@router.delete("/del_model_id") 
async def del_model(model_id: Modelid,current_user: SystemUser = Depends(get_current_user)):
    print('del_model') 
    model_id=model_id.id
    model = MongoAccess().del_model_id(model_id)

    download_model()
    return {'message':'model added'}
 
@router.post("/actif_model")
async def actif_model(current_user: SystemUser = Depends(get_current_user)):
    print('actif_model') 
    model_data = MongoAccess().phind_all_model()
    return json_util.dumps(model_data)
 