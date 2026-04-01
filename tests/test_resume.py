from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ✅ Test 1: Home API
def test_home():
    response = client.get("/")
    assert response.status_code == 200


# ✅ Test 2: Upload Resume
def test_upload_resume():
    response = client.post("/resume", json={
        "user_id": 1,
        "resume_link": "https://test.com/resume.pdf"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Resume uploaded successfully"


# ✅ Test 3: Get Resume
def test_get_resume():
    response = client.get("/resume/1")
    assert response.status_code == 200


# ✅ Test 4: Get Resume (Not Found)
def test_get_resume_not_found():
    response = client.get("/resume/999")
    assert response.status_code == 404


# ✅ Test 5: Invalid Resume Input
def test_invalid_resume():
    response = client.post("/resume", json={
        "user_id": "abc",   # wrong type
        "resume_link": "invalid-link"
    })
    assert response.status_code == 422