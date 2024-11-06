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

def test_postgresaccess():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchone.return_value = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser"
    }
    
    with patch("psycopg2.connect", return_value=mock_conn):
        postgress_access = PostgresAccess()
        assert isinstance(postgress_access.get_current_user(), dict)
        assert postgress_access.get_current_user()["email"] == "test@example.com"

@pytest.fixture
def mock_postgres():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchone.return_value = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser"
    }
    with patch("psycopg2.connect", return_value=mock_conn):
        yield mock_conn

def test_get_current_user(mock_postgres):
    user = PostgresAccess().get_current_user()
    assert user["email"] == "test@example.com"
