import os
os.environ["ENV"] = "test"

from fastapi.testclient import TestClient
from main import app

import pytest
from db.seed.seed import drop_and_seed_tables
from utils.jwt_utils import create_access_token

@pytest.fixture(autouse=True)
def seed_test_db():
    drop_and_seed_tables()

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def valid_credentials():
    return {
        "email": "user_c@example.com",
        "password": "password_c"
    }

@pytest.fixture()
def invalid_email():
    return{
        "email": "invalidemail@example.com",
        "password": "password_c"        
    }

@pytest.fixture()
def invalid_password():
    return{
        "email": "user_c@example.com",
        "password": "invalidpassword"        
    }

@pytest.fixture()
def no_password():
    return{
        "email": "user_c@example.com"  
    }

@pytest.fixture()
def no_email():
    return{
        "password": "invalidpassword"
    }

@pytest.fixture()
def register_existing_email():
    return{
        "name": "Alice Smith",
        "email": "user_c@example.com",
        "password": "securepassword123"
    }

@pytest.fixture()
def register_new_user():
    return{
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "securepassword123"
    }

@pytest.fixture()
def register_user_missing_email():
    return{
        "name": "Alice Smith",
        "password": "securepassword123"     
    }

@pytest.fixture()
def register_user_missing_name():
    return{
        "email": "alice@example.com",
        "password": "securepassword123"
    }

@pytest.fixture()
def register_user_missing_password():
    return{
        "name": "Alice Smith",
        "email": "alice@example.com",
    }

@pytest.fixture()
def get_auth_token_user_1():
    token = create_access_token(id=1)
    auth_headers = {"Authorization": f"Bearer {token}"}
    return auth_headers

@pytest.fixture()
def get_auth_token_user_2():
    token = create_access_token(id=2)
    auth_headers = {"Authorization": f"Bearer {token}"}
    return auth_headers
