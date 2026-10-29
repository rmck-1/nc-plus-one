def test_rsvp_with_valid_token_returns_201_status(client, get_auth_token_user_1):
    response = client.post("/events/1/rsvp", headers=get_auth_token_user_1)
    assert response.status_code == 201

def test_rsvp_with_invalid_token_returns_401_error(client):
    response = client.post("/events/1/rsvp", headers={"Authorization": "Bearer 123456789"})
    assert response.status_code == 401

def test_rsvp_with_invalid_event_id_returns_404_error(client, get_auth_token_user_1):
    response = client.post("/events/99/rsvp", headers=get_auth_token_user_1)
    assert response.status_code == 404

def test_rsvp_to_event_user_already_registered_to_returns_409_error(client, get_auth_token_user_1):
    response = client.post("/events/3/rsvp", headers=get_auth_token_user_1)
    assert response.status_code == 409

def test_rsvp_with_valid_token_and_valid_event_inserts_rsvp(client, get_auth_token_user_1):
    response = client.post("/events/1/rsvp", headers=get_auth_token_user_1)
    data = response.json()
    assert data["rsvp"]["id"] == 7
    assert data["rsvp"]["attendee_id"] == 1
    assert data["rsvp"]["event_id"] == 1
    assert isinstance(data["rsvp"]["created_at"], str)

def test_rsvp_with_no_header_returns_401_error(client):
    response = client.post("/events/1/rsvp")
    assert response.status_code == 401

def test_rsvp_with_string_event_id_returns_400_error(client, get_auth_token_user_1):
    response = client.post("/events/one/rsvp", headers=get_auth_token_user_1)
    assert response.status_code == 400
