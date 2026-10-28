def test_valid_login_credentials_returns_bearer_token(client, valid_credentials):
    response = client.post("/auth/login", json=valid_credentials)
    data = response.json()
    assert response.status_code == 200
    assert data["user_token"]["token_type"] == "bearer"

def test_invalid_email_returns_401_error(client, invalid_email):
    response = client.post("/auth/login", json=invalid_email)
    data = response.json()
    assert response.status_code == 401