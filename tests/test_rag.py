import pytest
from backend import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_backend_health():
    """Check if the backend API is responding."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_ask_endpoint_structure():
    """Verify the /ask endpoint accepts history and returns an answer."""
    payload = {
        "prompt": "Who is the main character?",
        "history": []
    }
    response = client.post("/ask", json=payload)
    assert response.status_code == 200
    assert "answer" in response.json()