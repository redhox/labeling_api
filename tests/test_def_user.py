import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from pydantic_settings import BaseSettings
from pydantic import BaseModel ,EmailStr
import pytest
from unittest.mock import Mock, patch

# Importation des fonctions et variables à tester
from app.api.def_util.def_user import (
    get_user, get_db_access, create_access_token, get_current_user,
    SECRET_KEY, ALGORITHM, SystemUser, PostgresAccess
)
import pytest
from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status

# Importation des fonctions et variables à tester
from app.api.def_util.def_user import (
    get_current_user, create_access_token, SECRET_KEY, ALGORITHM, PostgresAccess
)

@pytest.fixture
def mock_user():
    return {"email": "test@example.com", "username": "testuser"}

@pytest.fixture
def mock_token_data():
    # Simule un jeton valide avec une expiration dans le futur
    return {
        "sub": "test@example.com",
        "exp": int((datetime.utcnow() + timedelta(minutes=99999)).timestamp())
    }

@pytest.mark.asyncio
async def test_get_current_user_valid_token(mocker, mock_token_data, mock_user):
    # Mock jwt.decode pour qu'il retourne directement un payload valide avec expiration dans le futur
    mock_jwt_decode = mocker.patch('app.api.def_util.def_user.jwt.decode', return_value=mock_token_data)
    
    # Mock PostgresAccess.get_user_by_email pour retourner un utilisateur fictif
    mock_get_user_by_email = mocker.patch.object(PostgresAccess, 'get_user_by_email', return_value=mock_user)

    # Création d'un jeton pour le test
    token = create_access_token({"sub": "test@example.com"}, expires_delta=timedelta(minutes=99999))
    
    # Appel de la fonction get_current_user pour vérifier qu’elle renvoie un utilisateur valide
    user = await get_current_user(token=token)

    # Vérifications
    assert user == mock_user
    assert mock_jwt_decode.called  # Vérifie que decode a été appelé
    mock_get_user_by_email.assert_called_once_with("test@example.com")
