def test_get_events_request_returns_dictionary_with_all_events_in_list_as_value(client):
    response = client.get("/events")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert len(data["events"]) == 5

def test_get_events_returns_dictionary_list_ordered_by_start_date_ascending(client):
    response = client.get("/events")
    data = response.json()
    assert data["events"][0]["starts_at"] == "2025-12-31T23:30:00Z"

def test_get_events_venue_id_parameter_returns_dictionary_with_all_events_that_have_that_id(client):
    response = client.get("/events?venue_id=3")
    data = response.json()
    assert len(data["events"]) == 2

def test_get_events_organiser_id_parameter_returns_dictionary_with_all_events_that_have_that_id(client):
    response = client.get("/events?organiser_id=1")
    data = response.json()
    assert len(data["events"]) == 1

def test_get_events_returns_venue_details_joined_from_venues_table(client):
    response = client.get("/events")
    data = response.json()
    assert data["events"][0]["venue_name"] == "venue_b"
    assert data["events"][0]["venue_address"] == "address_b"
    assert data["events"][0]["venue_capacity"] == 50

def test_get_events_ID_returns_single_event_with_that_id(client):
    response = client.get("/events/2")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["event"]["title"] == "event_a"

def test_get_event_id_returns_venue_details_joined_from_venues_table(client):
    response = client.get("/events/2")
    data = response.json()
    assert data["event"]["venue_name"] == "venue_a"
    assert data["event"]["venue_address"] == "address_a"
    assert data["event"]["venue_capacity"] == 10

def test_get_events_id_returns_404_when_id_does_not_exist(client):
    response = client.get("/events/99")
    data = response.json()
    assert response.status_code == 404
    assert data["error"]["message"] == "Event not found"

def test_get_events_id_returns_400_when_invalid_str_input_provided(client):
    invalid_input = "one"
    response = client.get(f"/events/{invalid_input}")
    data = response.json()
    assert response.status_code == 400

def test_post_event_with_user_with_invalid_token_gets_401(client):
    response = client.post("/events", headers={"Authorization": "Bearer 123456789"})
    assert response.status_code == 401

def test_post_event_with_user_with_missing_token_gets_401(client):
    response = client.post("/events")
    assert response.status_code == 401

def test_post_event_with_missing_required_field_returns_400(client, get_token_and_partial_body_user_1):
    response = client.post("/events", headers=get_token_and_partial_body_user_1["headers"], json=get_token_and_partial_body_user_1["json"])
    assert response.status_code == 400

def test_post_event_with_invalid_date_format_returns_400(client, get_token_and_body_invalid_date_format_user_1):
    response = client.post("/events", headers=get_token_and_body_invalid_date_format_user_1["headers"], json=get_token_and_body_invalid_date_format_user_1["json"])
    assert response.status_code == 400

def test_post_event_with_valid_token_and_body_returns_201(client, get_token_and_body_user_1):
    response = client.post("/events", headers=get_token_and_body_user_1["headers"], json=get_token_and_body_user_1["json"])
    assert response.status_code == 201

def test_post_event_with_valid_token_and_body_returns_returns_expected_response(client, get_token_and_body_user_1):
    response = client.post("/events", headers=get_token_and_body_user_1["headers"], json=get_token_and_body_user_1["json"])
    data = response.json()
    assert response.status_code == 201
    assert data["event"]["id"] == 6
    assert data["event"]["title"] == "Summer Rooftop Social"
    assert data["event"]["description"] == "An evening of networking and good vibes."
    assert isinstance(data["event"]["starts_at"], str)
    assert isinstance(data["event"]["ends_at"], str)
    assert data["event"]["venue_id"] == 2
    assert data["event"]["organiser_id"] == 1
    assert isinstance(data["event"]["created_at"], str)
    assert response.headers["content-type"] == "application/json"

def test_post_event_with_venue_id_that_doesnt_exist_returns_404_error(client, get_token_and_body_user_1_invalid_venue):
    response = client.post("/events", headers=get_token_and_body_user_1_invalid_venue["headers"], json=get_token_and_body_user_1_invalid_venue["json"])
    assert response.status_code == 404

def test_patch_event_user_can_only_patch_their_own_events(client, patch_user_1_event_with_user_2):
    response = client.patch("/events/1", headers=patch_user_1_event_with_user_2["headers"], json=patch_user_1_event_with_user_2["json"])
    assert response.status_code == 403

def test_patch_event_user_with_missing_token_returns_401_error(client, patch_user_1_event):
    response = client.patch("/events/1", json=patch_user_1_event["json"])
    assert response.status_code == 401

def test_patch_event_user_with_invalid_token_returns_401_error(client, patch_user_1_event):
    response = client.patch("/events/1", headers={"Authorization": "Bearer 123456789"}, json=patch_user_1_event["json"])
    assert response.status_code == 401

def test_patch_event_event_with_invalid_date_format_returns_400_error(client, patch_user_1_event_with_invalid_date_format):
    response = client.patch("/events/1", headers=patch_user_1_event_with_invalid_date_format["headers"], json=patch_user_1_event_with_invalid_date_format["json"])
    assert response.status_code == 400

def test_patch_event_event_with_start_date_greater_than_end_date_returns_400_error(client, patch_user_1_event_with_start_date_greater):
    response = client.patch("/events/1", headers=patch_user_1_event_with_start_date_greater["headers"], json=patch_user_1_event_with_start_date_greater["json"])
    assert response.status_code == 400     

def test_patch_event_event_not_found_returns_404_error(client, patch_user_1_event):
    response = client.patch("/events/999", headers=patch_user_1_event["headers"], json=patch_user_1_event["json"])
    assert response.status_code == 404

def test_patch_event_with_valid_token_event_id_and_are_owner_returns_200(client, patch_user_1_event):
    response = client.patch("/events/1", headers=patch_user_1_event["headers"], json=patch_user_1_event["json"])
    data = response.json()
    assert response.status_code == 200
    assert data["event"]["title"] == "event_d"
    assert data["event"]["description"] == "An evening of networking and good vibes."
    assert isinstance(data["event"]["starts_at"], str)
    assert isinstance(data["event"]["ends_at"], str)
    assert data["event"]["organiser_id"] == 1
    assert response.headers["content-type"] == "application/json"    

def test_patch_event_with_empty_dict_body_returns_existing_event(client, patch_user_1_event_empty_body):
    response = client.patch("/events/1", headers=patch_user_1_event_empty_body["headers"], json=patch_user_1_event_empty_body["json"])
    data = response.json()    
    assert response.status_code == 200
    assert data["event"]["title"] == "event_d"

def test_patch_event_with_one_value_doesnt_overwrite_others_with_none(client, patch_user_1_event_only_1_field):
    response = client.patch("/events/1", headers=patch_user_1_event_only_1_field["headers"], json=patch_user_1_event_only_1_field["json"])
    data = response.json()
    assert response.status_code == 200
    assert data["event"]["title"] == "event_d"
    assert data["event"]["description"] == "An evening of networking and good vibes."
    assert data["event"]["starts_at"] is not None
    assert data["event"]["ends_at"] is not None

def test_patch_event_with_start_date_greater_than_end_date_but_no_end_date_provided_returns_400(client, patch_user_1_event_with_start_date_greater_no_end_date):
    response = client.patch("/events/1", headers=patch_user_1_event_with_start_date_greater_no_end_date["headers"], json=patch_user_1_event_with_start_date_greater_no_end_date["json"])
    assert response.status_code == 400

def test_patch_event_end_date_provided_and_no_start_date_but_end_date_is_less_than_start_date(client, patch_user_1_event_with_end_date_lesser_no_start_date):
    response = client.patch("/events/1", headers=patch_user_1_event_with_end_date_lesser_no_start_date["headers"], json=patch_user_1_event_with_end_date_lesser_no_start_date["json"])
    assert response.status_code == 400