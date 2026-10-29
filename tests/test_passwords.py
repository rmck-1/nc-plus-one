def test_valid_login_credentials_returns_bearer_token(client, valid_credentials):
    response = client.post("/auth/login", json=valid_credentials)
    data = response.json()
    assert response.status_code == 200
    assert data["user_token"]["token_type"] == "bearer"

def test_invalid_email_returns_401_error(client, invalid_email):
    response = client.post("/auth/login", json=invalid_email)
    data = response.json()
    assert response.status_code == 401
    assert data["error"]["message"] == "Incorrect email or password"

def test_invalid_password_returns_401_error(client, invalid_password):
    response = client.post("/auth/login", json=invalid_password)
    data = response.json()
    assert response.status_code == 401
    assert data["error"]["message"] == "Incorrect email or password"

def test_missing_email_returns_400_error(client, no_email):
    response = client.post("/auth/login", json=no_email)
    data = response.json()
    assert response.status_code == 400
    assert data["error"][0]["message"] == "The 'email' field is required"

def test_missing_password_returns_400_error(client, no_password):
    response = client.post("/auth/login", json=no_password)
    data = response.json()
    assert response.status_code == 400
    assert data["error"][0]["message"] == "The 'password' field is required"

def test_register_user_with_email_already_in_user_tablet_returns_409_error(client, register_existing_email):
    response = client.post("/auth/register", json=register_existing_email)
    data = response.json()
    assert response.status_code == 409

def test_register_user_with_unqique_email_returns_201(client, register_new_user):
    response = client.post("/auth/register", json=register_new_user)
    data = response.json()
    assert response.status_code == 201

def test_register_user_successfully_responds_with_id_name_email_created_fields(client, register_new_user):
    response = client.post("/auth/register", json=register_new_user)
    data = response.json()
    assert isinstance(data["user"]["id"], int)
    assert data["user"]["name"] == "Alice Smith"
    assert data["user"]["email"] == "alice@example.com"
    assert isinstance(data["user"]["created_at"], str)

def test_register_user_with_missing_email_responds_with_400_error(client,register_user_missing_email):
    response = client.post("/auth/register", json=register_user_missing_email)
    data = response.json()    
    assert response.status_code == 400
    assert data["error"][0]["message"] == "The 'email' field is required"

def test_register_user_with_missing_name_responds_with_400_error(client,register_user_missing_name):
    response = client.post("/auth/register", json=register_user_missing_name)
    data = response.json()    
    assert response.status_code == 400
    assert data["error"][0]["message"] == "The 'name' field is required"

def test_register_user_with_missing_password_responds_with_400_error(client,register_user_missing_password):
    response = client.post("/auth/register", json=register_user_missing_password)
    data = response.json()    
    assert response.status_code == 400
    assert data["error"][0]["message"] == "The 'password' field is required"
