from fastapi.testclient import TestClient

from ..main import app

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