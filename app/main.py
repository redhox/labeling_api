#crudAPI.py

from fastapi import FastAPI , HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.api.endpoints import users
from app.api.endpoints import images
from app.api.endpoints import models

from app.connector.connectorBDD_image import MongoAccess
from app.connector.connectorBucket import MinioBucketManager

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


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(images.router, prefix="/images", tags=["images"])
app.include_router(models.router, prefix="/models", tags=["models"])

@app.get("/")
async def root():
    return {"message": "api up"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)