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



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()





@router.post("/token", response_model=Token)
def login_for_access_token(data:UserLogin): 
 
    user = PostgresAccess().authenticate_user(data.email,data.password)
    print('tocken ',user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    last_login_db=PostgresAccess().get_last_login(user['id'])
    last_login= {}
    if last_login_db == None:
        last_login['message'] ='first conection'
    else:
        last_login['message'] =last_login_db[2]
        last_login['ip'] =last_login_db[3]
        last_login['uuid']=last_login_db[4]
        last_login['navigateur']=last_login_db[5]
    print('lastlogin',last_login)
    PostgresAccess().login(user['id'], data.ip_address, data.user_agent,data.uuid_machine)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
     
    access_token = manager.create_access_token(
        data={"sub": user['email']}
    )
    reponse = {'access_token': access_token, 'token_type': 'bearer','last_login':last_login}
    print('reponce',reponse)
    return reponse

    # access_token = create_access_token(
    #     data={"sub": user['email']}, expires_delta=access_token_expires
    # )
    # return {"access_token": access_token, "token_type": "bearer"}




# async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         token_data = TokenPayload(**payload)
        
#         if datetime.fromtimestamp(token_data.exp) < datetime.now():
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     user: Union[dict[str, Any], None] = db.get(token_data.sub, None)
    
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Could not find user",
#         )
    
#     return SystemUser(**user)

@router.post("/protected_route")
async def protected_route(user=Depends(manager)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non autorisé")
    print("protectedroute")
    print('bonjour', user)
    return user

 
# fin test #######################################################################
 
@router.post("/", response_model=UserDisplay, status_code=201)
async def create_user(user_data: UserCreate, db=Depends(get_db_access),current_user: SystemUser = Depends(get_current_user)):
    """
    Crée un nouvel utilisateur dans la base de données.

    Args:
        user_data (UserCreate): Données de l'utilisateur à créer, validées par le modèle UserCreate.
        db: Instance de la connexion à la base de données, obtenue par dépendance.

    Returns:
        UserDisplay: Les données de l'utilisateur créé, formatées selon le modèle UserDisplay.
    """
    print('create_user') 
    username = user_data.username
    email = user_data.email
    password = user_data.password
    new_user = PostgresAccess().create_user(username, email, password)

    # user_crud = UserCRUD(db.users_collection)  # Créez une instance de UserCRUD avec la collection MongoDB
    # new_user = user_crud.create_user(user_data)
    
    return JSONResponse(content=jsonable_encoder(new_user))


@router.get("/", response_model=List[UserDisplay])
async def read_all_users(db=Depends(get_db_access),current_user: SystemUser = Depends(get_current_user)): 
    """
    Récupère une liste de tous les utilisateurs enregistrés dans la base de données.

    Args:
        db: Instance de la connexion à la base de données, obtenue par dépendance.

    Returns:
        List[UserDisplay]: Liste des utilisateurs, chacun formaté selon le modèle UserDisplay.
    """
    
    """
    Endpoint to retrieve all users from the database.

    Returns:
        JSON: A JSON object containing the user data.
    """
    users = PostgresAccess().get_all_users()

    return JSONResponse(content=jsonable_encoder(users))
    # Convertit chaque document MongoDB en modèle UserDisplay, en assumant UserDisplay peut être initialisé directement avec ces documents
    # return [UserDisplay(**user) for user in users]


@router.post("/ids")
async def read_user_by_id(user_id: Userid,current_user: SystemUser = Depends(get_current_user)):
    """
    Récupère les données d'un utilisateur spécifique par son ID.

    Args:
        user_id (str): ID de l'utilisateur à récupérer.
        db: Instance de la connexion à la base de données, obtenue par dépendance.

    Returns:
        UserDisplay: Les données de l'utilisateur demandé, formatées selon le modèle UserDisplay.

    Raises:
        HTTPException: Si aucun utilisateur n'est trouvé avec l'ID fourni.
    """
    print('read_user_by_id ',user_id)

    user = PostgresAccess().get_user_by_id(user_id)
    return JSONResponse(content=jsonable_encoder(user))


@router.post("/get_all_users", response_model=List[UserDisplay])
async def get_all_users(current_user: SystemUser = Depends(get_current_user)):

    print('get_all_users ')

    user = PostgresAccess().get_all_users()
    return JSONResponse(content=jsonable_encoder(user))



@router.post("/email", response_model=UserDisplay,status_code=201)
async def read_user_by_email(user_email: Usermail, db=Depends(get_db_access),current_user: SystemUser = Depends(get_current_user)):
    """
    Récupère les données d'un utilisateur spécifique par son adresse email.

    Args:
        email (str): Email de l'utilisateur à récupérer.
        db: Instance de la connexion à la base de données, obtenue par dépendance.

    Returns:
        UserDisplay: Les données de l'utilisateur demandé, formatées selon le modèle UserDisplay.

    Raises:
        HTTPException: Si aucun utilisateur n'est trouvé avec l'email fourni.
    """
    
    user_email=user_email.email
    user = PostgresAccess().get_user_by_email(user_email)
    return JSONResponse(content=jsonable_encoder(user))


@router.delete("/delete")
async def delete_user_by_id(user_id: Userid, db=Depends(get_db_access),current_user: SystemUser = Depends(get_current_user)):
    """
     Supprime un utilisateur spécifique par son ID.

     Args:
         user_id (str): ID de l'utilisateur à supprimer.
         db: Instance de la connexion à la base de données, obtenue par dépendance.

     Returns:
         bool: True si la suppression a réussi, False sinon.

     Raises:
         HTTPException: Si la suppression échoue ou si aucun utilisateur n'est trouvé avec l'ID fourni.
     """
    print('delete_user_by_id',user_id.user_id)
    user = PostgresAccess().delete_user_by_id(user_id.user_id)
    return JSONResponse(content=jsonable_encoder(user))



@router.put("/switch_role")
async def switch_role(request: SwitchRoleRequest,db=Depends(get_db_access),current_user: SystemUser = Depends(get_current_user)):
    """
     Supprime un utilisateur spécifique par son ID.

     Args:
         user_id (str): ID de l'utilisateur à supprimer. 
         db: Instance de la connexion à la base de données, obtenue par dépendance.

     Returns:
         bool: True si la suppression a réussi, False sinon.

     Raises:
         HTTPException: Si la suppression échoue ou si aucun utilisateur n'est trouvé avec l'ID fourni.
     """
    user_id = request.user_id
    role = request.role_is_admin
    user = PostgresAccess().switch_role_by_id(user_id,role)
    return JSONResponse(content=jsonable_encoder(user))

@router.post("/login", response_model=UserDisplay)
async def login_user(data:UserLogin):
    """
    Authentifie un utilisateur en vérifiant son nom d'utilisateur et son mot de passe.

    Args:
        username (str): Le nom d'utilisateur de l'utilisateur.
        password (str): Le mot de passe de l'utilisateur.
        db: Instance de la connexion à la base de données, obtenue par dépendance.

    Returns:
        UserDisplay: Les données de l'utilisateur si les identifiants sont valides.

    Raises:
        HTTPException: Si les identifiants ne sont pas valides.
    """
    print("login")
    
    try:
        user = PostgresAccess().authenticate_user(data.email, data.password)
        # Si l'authentification réussit, retourner les données de l'utilisateur
        print("login",user)
        return JSONResponse(content=jsonable_encoder(user))
    except HTTPException as e:
        # Si une exception HTTP est levée (par exemple, si l'utilisateur n'est pas trouvé ou si le mot de passe est incorrect),
        # relancer l'exception avec un code de statut 401 (Non autorisé) pour indiquer une tentative de connexion échouée
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e.detail))
