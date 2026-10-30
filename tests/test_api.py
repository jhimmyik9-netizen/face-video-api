from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_rejects_unsupported_extension():
    response = client.post(
        "/analyze",
        files={"file": ("notes.txt", b"not a video", "text/plain")},
    )
    assert response.status_code == 415


def test_analyze_rejects_empty_file():
    response = client.post(
        "/analyze",
        files={"file": ("empty.mp4", b"", "video/mp4")},
    )
    assert response.status_code == 400
