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

from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status

# Importation des fonctions et variables à tester
from app.api.def_util.def_user import (
    get_current_user, create_access_token, SECRET_KEY, ALGORITHM, PostgresAccess
)
from datetime import datetime, timedelta
from app.api.def_util.def_user import (
    get_current_user, create_access_token, SECRET_KEY, ALGORITHM, PostgresAccess
)

from unittest.mock import MagicMock, patch
# Mock PostgresAccess at the module level, so it’s replaced in all imports
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

import pytest
from unittest.mock import MagicMock
from app.api.def_util.def_user import PostgresAccess

import pytest
from unittest.mock import MagicMock
from app.api.def_util.def_user import PostgresAccess



import unittest.mock as mock

import os
import psycopg2
from unittest.mock import MagicMock

class PostgresAccess:
    def __init__(self):
        if os.environ.get('SKIP_POSTGRES_CONNECTION', 'false') == 'true':
            self.conn = MagicMock()
            self.cursor = self.conn.cursor.return_value
            self.cursor.fetchone.return_value = {
                "id": 1,
                "email": "test@example.com",
                "username": "testuser"
            }
        else:
            # Connexion réelle à PostgreSQL si SKIP_POSTGRES_CONNECTION n'est pas défini
            self.conn = psycopg2.connect(
                dbname=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                host=os.environ['DB_HOST'],
                port=os.environ['DB_PORT']
            )

    def get_current_user(self):
        if hasattr(self, 'conn'):
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = 1;")
            result = cursor.fetchone()
            assert result is not None, "User not found in database"
            return {"email": result["email"], "username": result["username"]}
        else:
            # Simuler la réponse sans connexion réelle
            return {"email": "test@example.com", "username": "testuser"}

# Dans vos tests, utilisez cette classe PostgresAccess avec l'environnement modifié
os.environ['SKIP_POSTGRES_CONNECTION'] = 'true'
