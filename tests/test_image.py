import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.routing import APIRouter
# from app.router import router  # Adjust the import to your router location
from bson import ObjectId
# from app.api.endpoints import users
from app.api.endpoints.images import router
from pydantic_settings import BaseSettings

# from app.api.endpoints import models
# Create a FastAPI app instance and include the router
app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Mocking the MongoAccess and MinioBucketManager for testing
class MockMongoAccess:
    @staticmethod
    def phind_path(path):
        if path == "existing_path":
            return {"_id": ObjectId(), "regions": []}
        return None

    @staticmethod
    def incert_image(data):
        return {"status": "success"}

    @staticmethod
    def change_label(image_id, regions):
        return {"status": "updated"}

class MockMinioBucketManager:
    @staticmethod
    def upload_file(local_path, bucket_path):
        return {"status": "uploaded"}

# Override the MongoAccess and MinioBucketManager in the router
def override_dependencies():
    return MockMongoAccess(), MockMinioBucketManager()

@app.get("/override_dependencies")
async def dependency_override():
    return override_dependencies()

# Tests for the /post_resultat endpoint
def test_post_resultat(client):
    response = client.put("/post_resultat", json={
        "filename": "test_image.jpg",
        "filedir": "/images/",
        "path": "existing_path",
        "regions": [],
        "uuid_machine": "uuid-1234"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"  # Change this line
    assert response.json()["action"] == "updated" 

def test_post_resultat_not_found(client):
    response = client.put("/post_resultat", json={
        "filename": "test_image.jpg",
        "filedir": "/images/",
        "path": "non_existing_path",
        "regions": [],
        "uuid_machine": "uuid-1234"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

# Tests for the /image_save endpoint
def test_image_save_on_bucket(client):
    with open("test_image.jpg", "wb") as f:
        f.write(b"test image data")
    
    with open("test_image.jpg", "rb") as f:
        response = client.post("/image_save", files={
            "file": ("test_image.jpg", f, "image/jpeg"),
        }, data={
            "path": "path/to/save",
            "model": "test_model"
        })
    
    assert response.status_code == 200 # Assuming label_image returns this key

# Tests for the /image_search endpoint
def test_image_search(client):
    response = client.post("/image_search", data={"path": "existing_path"})
    assert response.status_code == 200
    assert "_id" in response.json()



# Tests for the /labels endpoint
def test_image_labels(client):
    response = client.post("/labels", json={
        "uuid": "uuid-1234",
        "projet_name": "test_project",
        "download": False
    })
    assert response.status_code == 200
    assert "message" in response.json()

# Cleanup test file if necessary
import os

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists("test_image.jpg"):
        os.remove("test_image.jpg")
