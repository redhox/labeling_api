#crudAPI.py

from fastapi import FastAPI , HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.api.endpoints import users
from app.api.endpoints import images

from app.connector.connectorBDD_image import MongoAccess

import os
from dotenv import load_dotenv

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()
mongo_access = MongoAccess()
mongo_access.initialize_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet à toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes
    allow_headers=["*"],  # Permet tous les headers
)



#test tocken #########################################################################
# class Token(BaseModel):
#     access_token: str
#     token_type: str

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
# @app.get("/get_token")
# async def get_token():
#     data = {'info': 'informations secrètes', 'from': 'GFG'}
#     token = create_access_token(data=data)
#     return {'token': token}
# @app.post("/verify_token")
# async def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.post("/token/")
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     # Implémentation de la génération de token
#     print('bonjour')
# @app.get("/secure/")
# def secure_endpoint(token: str = Depends(oauth2_scheme)):
#     print('bonjour')






#fin test tocken #########################################################################


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
async def root():
    return {"message": "Welcome to Manag'IA API service"}

# users_db = {
#     "johndoe": {
#         "id": 1,
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "role": 1,
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)