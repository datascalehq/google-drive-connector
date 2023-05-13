import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
path = "/files_and_folders"

def test_get_files_and_folders_success():
    shared_url = "https://drive.google.com/drive/folders/19rxOEL_yeFAMZXjsybCUB_TW9cVMA5Uc?usp=sharing"
    response = client.get(path, params={"shared_url": shared_url})
    assert response.status_code == 200

    response_dict = response.json()
    assert "structure_tree" in response_dict
    assert "file_nodes" in response_dict

def test_get_files_and_folders_with_no_permission_url():
    shared_url = "https://drive.google.com/drive/folders/123?usp=sharing"
    response = client.get(path, params={"shared_url": shared_url})
    assert response.status_code == 400
    
    response_dict = response.json()
    assert response_dict["error_code"] == ""
    assert response_dict["error_message"] == "folder_id: 123 cant access by server"

def test_get_files_and_folders_without_shared_url():
    response = client.get(path)
    assert response.status_code == 422