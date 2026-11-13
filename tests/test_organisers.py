# def test_get_organiser_stats_with_user_with_missing_token_returns_401_error(client):
#     response = client.get("/organisers/1/stats")
#     assert response.status_code == 401

# def test_get_organiser_stats_with_user_with_invalid_token_returns_401_error(client):
#     response = client.get("/organisers/1/stats", headers={"Authorization": "Bearer 123456789"})
#     assert response.status_code == 401

# def test_get_organiser_stats_returns_correct_stats_of_user_events(client, get_auth_token_user_1):
#     response = client.get("organisers/1/stats", headers=get_auth_token_user_1)
#     data = response.json()
#     assert data["stats"][0]["organiser_id"] == 1
#     assert data["stats"][0]["name"] == "user_c"
#     assert data["stats"][0]["total_events"] == 1
#     assert data["stats"][0]["avg_attendance"] == 0