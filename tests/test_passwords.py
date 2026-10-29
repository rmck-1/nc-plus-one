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