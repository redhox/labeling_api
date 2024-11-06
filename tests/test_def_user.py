import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from pydantic_settings import BaseSettings
from pydantic import BaseModel ,EmailStr
import pytest
from unittest.mock import Mock, patch
import python_multipart
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
import psycopg2
import pytest
import os
from contextlib import contextmanager

# Fixture pour la connexion à la base de données
@pytest.fixture(scope="module")
def db_connection():
    # Vous pouvez récupérer l'URL de connexion à partir des variables d'environnement ou d'une configuration
    db_url = os.getenv("DATABASE_URL", "postgresql://testuser:testpassword@localhost:5432/testdb")
    
    # Créer une connexion à PostgreSQL
    connection = psycopg2.connect(db_url)
    
    # Assurez-vous que la connexion est fermée après les tests
    yield connection
    connection.close()

# Fixture pour un utilisateur fictif
@pytest.fixture
def mock_user():
    return {"email": "test@example.com", "username": "testuser"}

# Fixture pour simuler un jeton
@pytest.fixture
def mock_token_data():
    from datetime import datetime, timedelta
    return {
        "sub": "test@example.com",
        "exp": int((datetime.utcnow() + timedelta(minutes=99999)).timestamp())
    }
def test_get_current_user_valid_token(db_connection, mock_user, mock_token_data):
    # Exemple de test qui nécessite la connexion à la base de données
    with db_connection.cursor() as cursor:
        # Vous pouvez aussi exécuter une requête d'insertion pour préparer des données avant le test
        cursor.execute("SELECT * FROM users WHERE email = %s;", (mock_user['email'],))
        result = cursor.fetchone()

        # Vérifiez que l'utilisateur existe
        assert result is not None
        assert result[1] == mock_user["email"]  # Assumons que l'email est à la position 1
        assert result[2] == mock_user["username"]  # Assumons que le username est à la position 2
