def test_user_with_missing_token_returns_401_error(client):
    response = client.get("/user/me/events")
    assert response.status_code == 401

def test_user_with_invalid_token_returns_401_error(client):
    response = client.get("/user/me/events", headers={"Authorization": "Bearer 123456789"})
    assert response.status_code == 401

def test_user_with_valid_token_returns_list_of_their_enriched_events(client, get_auth_token_user_1):
    response = client.get("/user/me/events", headers=get_auth_token_user_1)
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data["events"], list)
    assert data["events"][0]["total_rsvps"] == 2
    assert data["events"][0]["event_rank"] == 1
    assert len(data["events"]) == 2
    assert data["events"][1]["event_rank"] == 2
    assert data["events"][0]["starts_at"] < data["events"][1]["starts_at"]

def test_user_with_no_rsvps_returns_empty_list_and_200_status_code(client, get_auth_token_user_1):
    client.delete("/events/3/rsvp/me", headers=get_auth_token_user_1)
    client.delete("/events/5/rsvp/me", headers=get_auth_token_user_1)
    response = client.get("/user/me/events", headers=get_auth_token_user_1)
    data = response.json()
    assert response.status_code == 200 
    assert data["events"] == []