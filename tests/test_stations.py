import pytest

VALID = {"code": "ST-001", "name": "test", "capacity" : 10}

def create(client, **overrides):
    return client.post("/stations", json={**VALID, **overrides})

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def testcreateandgetbyid(client):
    created = create(client)
    assert created.status_code == 201
    body = created.json()
    assert body["code"] == "ST-001"
    assert body["status"] == "open"

    fetched = client.get(f"/stations/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body

def testfilterbystatus(client):
    create(client, code="A", status="open")
    create(client, code="B", status="closed")
    create(client, code="C", status="open")

    response = client.get("/stations", params={"status": "open"})
    assert response.status_code == 200
    stations = response.json()
    assert {s["code"] for s in stations} == {"A", "C"}
    assert all(s["status"] == "open" for s in stations)

def testpatchnameonly(client):
    original = create(client, status="maintenance").json()

    response = client.patch(f"/stations/{original['id']}", json={"name": "test"})
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "test"
    assert updated["code"] == original["code"]
    assert updated["capacity"] == original["capacity"]
    assert updated["status"] == original["status"]

def testgetunknidreturnsjs404(client):
    response = client.get("/stations/9999")
    assert response.status_code == 404
    assert "detail" in response.json()

@pytest.mark.parametrize(
    "field, value", [("capacity", 0), ("status", "flying")],
)

def testinvldinputreturns422(client, field, value):
    response = create(client, **{field: value})
    assert response.status_code == 422
    assert client.get("/stations").json() == []

def testdplctcodereturns409(client):
    assert create(client).status_code == 201
    assert create(client, name="jsp").status_code == 409
    assert len(client.get("/stations").json()) == 1