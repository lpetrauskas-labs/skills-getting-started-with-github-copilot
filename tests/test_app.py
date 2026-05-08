import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Resetar o banco em memória antes de cada teste
    for activity in activities.values():
        activity['participants'].clear()
        # Restaurar participantes iniciais se desejar

client = TestClient(app)

def test_get_activities():
    # Arrange
    # Nenhum setup extra necessário
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_participant():
    # Arrange
    email = "novo@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate_participant():
    # Arrange
    email = "dup@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_participant():
    # Arrange
    email = "remover@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Removed" in response.json()["message"]

def test_unregister_nonexistent_participant():
    # Arrange
    email = "naoexiste@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
