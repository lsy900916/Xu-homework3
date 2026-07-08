def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Todo App API"


def test_create_todo_endpoint(client):
    response = client.post("/api/todos/", json={"title": "API item"})
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "API item"
    assert data["completed"] is False
    assert "id" in data

    list_response = client.get("/api/todos/")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1


def test_create_todo_empty_title(client):
    response = client.post("/api/todos/", json={"title": "  "})
    assert response.status_code == 400


def test_update_and_delete_todo_endpoint(client):
    response = client.post("/api/todos/", json={"title": "Update me"})
    todo_id = response.json()["id"]

    update_response = client.put(f"/api/todos/{todo_id}", json={"completed": True})
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200

    not_found_response = client.delete(f"/api/todos/{todo_id}")
    assert not_found_response.status_code == 404


def test_clear_endpoints(client):
    client.post("/api/todos/", json={"title": "Done item", "completed": True})
    client.post("/api/todos/", json={"title": "Todo item", "completed": False})

    clear_completed_response = client.delete("/api/todos/clear-completed")
    assert clear_completed_response.status_code == 200
    assert clear_completed_response.json()["deleted_count"] == 1

    clear_all_response = client.delete("/api/todos/clear-all")
    assert clear_all_response.status_code == 200
    assert clear_all_response.json()["deleted_count"] == 2
