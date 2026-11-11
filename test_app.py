import pytest
from app import app
from db import init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"URL Shortener" in response.data

def test_shorten_valid_url(client):
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "code" in data
    assert "short_url" in data
    assert len(data["code"]) == 6

def test_shorten_auto_prepend_https(client):
    response = client.post("/shorten", json={"url": "github.com"})
    assert response.status_code == 201
    code = response.get_json()["code"]

    stats_res = client.get(f"/stats/{code}")
    assert stats_res.status_code == 200
    assert stats_res.get_json()["original_url"] == "https://github.com"

def test_shorten_invalid_scheme(client):
    response = client.post("/shorten", json={"url": "ftp://files.example.com"})
    assert response.status_code == 400
    assert "invalid url scheme" in response.get_json()["message"]

def test_shorten_missing_or_invalid_payload(client):
    res1 = client.post("/shorten", json={})
    assert res1.status_code == 400

    res2 = client.post("/shorten", json={"url": ""})
    assert res2.status_code == 400

    res3 = client.post("/shorten", data="plain text not json", content_type="text/plain")
    assert res3.status_code == 400

def test_redirect_and_click_tracking(client):
    shorten_res = client.post("/shorten", json={"url": "https://python.org"})
    code = shorten_res.get_json()["code"]

    # Check stats before any clicks
    stats_before = client.get(f"/stats/{code}")
    assert stats_before.status_code == 200
    assert stats_before.get_json()["clicks"] == 0

    # Perform redirect
    redirect_res = client.get(f"/{code}")
    assert redirect_res.status_code == 302
    assert redirect_res.headers["Location"] == "https://python.org"

    # Check stats after click
    stats_after = client.get(f"/stats/{code}")
    assert stats_after.status_code == 200
    assert stats_after.get_json()["clicks"] == 1

def test_redirect_not_found(client):
    response = client.get("/nonexistent123")
    assert response.status_code == 404

def test_stats_not_found(client):
    response = client.get("/stats/nonexistent123")
    assert response.status_code == 404

