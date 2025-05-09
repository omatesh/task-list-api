# test_get_goal_not_found

# @pytest.mark.skip(reason="test to be completed by student")
# def test_get_goal_not_found(client):
#     # Act
#     response = client.get("/goals/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 404
#     assert response_body == {"message": "Goal 1 not found"}

# # test_update_goal

# @pytest.mark.skip(reason="test to be completed by student")
# def test_update_goal(client, one_goal):
#     # Act
#     response = client.put("/goals/1", json={"title": "Updated Goal Title"})

#     # Assert
#     assert response.status_code == 200

#     response_body = response.get_json()
#     assert "goal" in response_body
#     assert response_body == {
#         "goal": {
#             "id": 1,
#             "title": "Updated Goal Title"
#         }
#     }

# # test_update_goal_not_found

# @pytest.mark.skip(reason="test to be completed by student")
# def test_update_goal_not_found(client):
#     # Act
#     response = client.put("/goals/1", json={"title": "Updated Goal Title"})
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 404
#     assert response_body == {"message": "Goal 1 not found"}


# # test_delete_goal (Complete response body check)

# @pytest.mark.skip(reason="No way to test this feature yet")
# def test_delete_goal(client, one_goal):
#     # Act
#     response = client.delete("/goals/1")

#     # Assert
#     assert response.status_code == 204

#     # Confirm deletion
#     response = client.get("/goals/1")
#     assert response.status_code == 404

#     response_body = response.get_json()
#     assert response_body == {"message": "Goal 1 not found"}


# # test_delete_goal_not_found

# @pytest.mark.skip(reason="test to be completed by student")
# def test_delete_goal_not_found(client):
#     # Act
#     response = client.delete("/goals/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 404
#     assert response_body == {"message": "Goal 1 not found"}