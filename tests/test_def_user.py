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

class PostgresAccess:
    def __init__(self):
        self.conn = mock.Mock()
        self.cursor = self.conn.cursor.return_value
        self.cursor.fetchone.return_value = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser"
        }
def test_postgresaccess():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser"
    }
    
    # Simuler la méthode cursor()
    mock_conn.cursor.return_value = mock_cursor
    
    # Simuler la méthode execute()
    mock_conn.execute = lambda *args, **kwargs: None
    
    # Simuler la méthode fetchone()
    mock_conn.fetchone = lambda self: mock_cursor.fetchone().fetchall()[0]
    
    # Simuler la méthode close()
    mock_conn.close = lambda: None
    
    with patch("psycopg2.connect", return_value=mock_conn):
        postgress_access = PostgresAccess()
        assert isinstance(postgress_access.get_current_user(), dict)
        assert postgress_access.get_current_user()["email"] == "test@example.com"

@pytest.fixture
def mock_postgres():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Simuler la méthode cursor()
    mock_conn.cursor.return_value = mock_cursor
    
    # Simuler les méthodes de cursor()
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser"
    }
    mock_cursor.fetchall.return_value = []
    mock_cursor.close.return_value = None
    
    # Simuler la méthode close()
    mock_conn.close.return_value = None
    
    with patch("psycopg2.connect", return_value=mock_conn):
        yield mock_conn

def test_get_current_user(mock_postgres):
    user = PostgresAccess().get_current_user()
    assert user["email"] == "test@example.com"
