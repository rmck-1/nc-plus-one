import os
os.environ["ENV"] = "test"

from fastapi.testclient import TestClient
from main import app

import pytest
from db.seed.seed import drop_and_seed_tables

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
        "password": "invalidpassword"   
    }

@pytest.fixture()
def no_email():
    return{
        "email": "user_c@example.com",   
    }