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
def get_token_and_body_user_1():
    token = create_access_token(id=1)
    body = {
       "title": "Summer Rooftop Social",
       "description": "An evening of networking and good vibes.",
       "starts_at": "2025-08-15T18:00:00Z",
       "ends_at": "2025-08-15T21:00:00Z",
       "venue_id": 2
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def get_token_and_partial_body_user_1():
    token = create_access_token(id=1)
    body = {
       "title": "Summer Rooftop Social",
       "description": "An evening of networking and good vibes.",
       "starts_at": "2025-08-15T18:00:00Z",
       "ends_at": "2025-08-15T21:00:00Z"
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def get_token_and_body_invalid_date_format_user_1():
    token = create_access_token(id=1)
    body = {
       "title": "Summer Rooftop Social",
       "description": "An evening of networking and good vibes.",
       "starts_at": "30/10/2026",
       "ends_at": "2025-08-15T21:00:00Z",
       "venue_id" "venue_id": 2
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def get_token_and_body_user_1_invalid_venue():
    token = create_access_token(id=1)
    body = {
       "title": "Summer Rooftop Social",
       "description": "An evening of networking and good vibes.",
       "starts_at": "2025-08-15T18:00:00Z",
       "ends_at": "2025-08-15T21:00:00Z",
       "venue_id": 999
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event():
    token = create_access_token(id=1)
    body = {
       "description": "An evening of networking and good vibes.",
       "starts_at": "2025-08-15T18:00:00Z",
       "ends_at": "2025-08-15T21:00:00Z"
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event_empty_body():
    token = create_access_token(id=1)
    body = {
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event_with_user_2():
    token = create_access_token(id=2)
    body = {
       "description": "An evening of networking and good vibes.",
       "starts_at": "2025-08-15T18:00:00Z",
       "ends_at": "2025-08-15T21:00:00Z"
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event_only_1_field():
    token = create_access_token(id=1)
    body = {
       "description": "An evening of networking and good vibes.",
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event_with_invalid_date_format():
    token = create_access_token(id=1)
    body = {
       "description": "An evening of networking and good vibes.",
       "starts_at": "30/10/2026",
       "ends_at": "2025-08-15T21:00:00Z"
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event_with_start_date_greater():
    token = create_access_token(id=1)
    body = {
       "description": "An evening of networking and good vibes.",
       "starts_at": "2026-08-15T18:00:00Z",
       "ends_at": "2025-08-15T21:00:00Z"
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event_with_start_date_greater_no_end_date():
    token = create_access_token(id=1)
    body = {
       "description": "An evening of networking and good vibes.",
       "starts_at": "2026-08-15T18:00:00Z",
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}

@pytest.fixture()
def patch_user_1_event_with_end_date_lesser_no_start_date():
    token = create_access_token(id=1)
    body = {
       "description": "An evening of networking and good vibes.",
       "ends_at": "2023-08-15T18:00:00Z",
    }
    return {"headers": {"Authorization": f"Bearer {token}"},
            "json": body}