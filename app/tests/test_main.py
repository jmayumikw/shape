from fastapi.testclient import TestClient
import pytest

from ..main import app
from ..main import find_key

client = TestClient(app)

def test_encode_with_success():
  response = client.get("/encode/99999999")
  assert response.status_code == 200
  assert response.json() == { "encode": "-C$DTW" }

def test_encode_with_invalid_input():
  response = client.get("/encode/abcdef")
  assert response.status_code == 422

def test_decode_with_success():
  response = client.get("/decode/-C$DTW")
  assert response.status_code == 200
  assert response.json() == { 'decode': 99999999 }

def test_decode_with_invalid_input_lenght():
  response = client.get("/decode/13a")
  assert response.status_code == 422
  assert response.json() == { "detail": "Invalid length"}

def test_decode_with_invalid_input():
  response = client.get("/decode/&t&t$b")
  assert response.status_code == 422
  assert response.json() == { "detail": "Invalid input"}

def test_find_key_with_success():
  assert find_key(0) == "A"

def test_find_key_with_invalid_input():
  with pytest.raises(Exception) as response:
    find_key("&")
  assert "Only integers are allowed" in str(response.value)
  assert response.type == TypeError
