def test_user_with_missing_token_returns_401_error(client):
    response = client.get("/organisers/1/stats")
    assert response.status_code == 401

def test_user_with_invalid_token_returns_401_error(client):
    response = client.get("/organisers/1/stats", headers={"Authorization": "Bearer 123456789"})
    assert response.status_code == 401