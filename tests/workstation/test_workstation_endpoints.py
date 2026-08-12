import random
import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

USERS_IDS = [
"01KZVQ603KWMPPD1Y38YA7DEME",
"01KZVRE1FV18RZC1NPGP45RVPZ",
"01KZVRE1KDNEQM1TRDS5T71BW4",
"01KZVRE1VQK2YN8M1B6GPNXPXV",
"01KZVRE25RSNS72RRJXVCGGNNQ",
"01KZVRE2BKGVFD6QZ9WKDBK80G",
"01KZVRE2HVS64469C7G08GE62W",
"01KZVRE2ZMRZVGE49BMTYJR4JG",
"01KZVRE35CQFZDZ27RH0E7SM14",
"01KZVRE3F09C21ZZXV3N0WC87W",
"01KZVRE3RC58J6VN7JHA4YRG67",
"01KZVRE460KXE1ENKCDFMSRHTS",
"01KZVSZA2N2MNK14GXXJ0NN6AG",
"01KZVSZAAQ2ZGXE4X40Y74EM02",
"01KZVSZAEGW2DE7ZACE8Q61Y49",
"01KZVSZAQX2GN26JA7RG2ATN4W",
"01KZVSZAXYXDK6W4BTZYA8F64C",
"01KZVSZB80QW3CPA4RB5Z05ZDW",
"01KZVSZBH6T959TRZ86CJXMKJX",
"01KZVSZBQKNHHGVMFGVFN24JB4",
"01KZVSZC0Z38S9JZW1CWAGNWW5",
"01KZVSZC9W22ZJN282CC7206YF",
"01KZVSZCT71J2Z0GH13M99ZZEK",
]

def random_users_id() -> str:
    return random.choice(USERS_IDS)

@pytest.fixture 
def client(): 
    with TestClient(app) as c: 
        yield c


@pytest.fixture
def workstation_payload() -> dict:
    """Payload mínimo válido para crear un workstation."""
    return {
        "user": random_users_id(),
        "description": "descripcion de prueba",
        "type": "DESKTOP",
        "area": "SUPPORT",
    }


@pytest.fixture
def created_workstation(workstation_payload, client) -> dict:
    """Crea un user real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/workstations/", json=workstation_payload)
    assert response.status_code == 201, f"Setup falló: {response.text}"
    return response.json()


class TestCreateWorkstation:
    # prueba el endpoint de post con todos los atributos
    def test_create_workstation_success(self, workstation_payload, client):
        response = client.post("/api/v1/workstations/", json=workstation_payload)
        assert response.status_code == 201
        data = response.json()
        print(data)
        assert data["description"] == workstation_payload["description"]
        assert data["status"] == "ACTIVE"
        assert "id" in data

    # prueba el endpoint de post sin los atributos opcionales
    def test_create_workstation_without_optional_fields(self, client):
        payload = {
            "user": random_users_id(),
            "type": "DESKTOP",
            "area": "SUPPORT",
        }
        response = client.post("/api/v1/workstations/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "ACTIVE"
        assert data["type"] == payload["type"]

    # prueba el endpoint de post sin el user, lanza error
    def test_create_workstation_missing_required_field(self, workstation_payload, client):
        payload = workstation_payload.copy()
        del payload["user"]
        response = client.post("/api/v1/workstations/", json=payload)
        assert response.status_code == 422   # Unprocessable Entity

    # prueba el endpoint de post si devuelve created_at y updated_at
    def test_create_workstation_returns_timestamps(self, client):
        payload = {
            "user": random_users_id(),
            "description": "descripcion de prueba",
            "type": "DESKTOP",
            "area": "SUPPORT"
        }
        response = client.post("/api/v1/workstations/", json=payload)
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllWorkstations:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, client):
        response = client.get("/api/v1/workstations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "workstations" in data
        assert isinstance(data["workstations"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_workstation
    def test_get_all_contains_created_workstation(self, created_workstation, client):
        response = client.get("/api/v1/workstations/")
        workstations = response.json()["workstations"]
        ids = [p["id"] for p in workstations]
        assert created_workstation["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_workstation_fields(self, created_workstation, client):
        response = client.get("/api/v1/workstations/")
        workstations = response.json()["workstations"]
        print(response.json())
        workstation = next((p for p in workstations if p["id"] == created_workstation["id"]), None)
        assert workstation is not None
        for field in ("id", "status", "type"):
            assert field in workstation


# ─── Obtener por ID ───────────────────────────────────────────────────────────

class TestGetWorkstationById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_workstation con su respectivo id
    def test_get_workstation_by_id_success(self, created_workstation, client):
        workstation_id = created_workstation["id"]
        response = client.get(f"/api/v1/workstations/{workstation_id}")
        assert response.status_code == 200
        assert response.json()["id"] == workstation_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_workstation_by_id_not_found(self, client):
        response = client.get("/api/v1/workstations/id-que-no-existe-99999")
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_workstation
    def test_get_workstation_by_id_returns_correct_data(self, created_workstation, client):
        response = client.get(f"/api/v1/workstations/{created_workstation['id']}")
        data = response.json()
        assert data["description"] == created_workstation["description"]


class TestUpdateWorkstation:
# prueba el endpoint de patch para actualizar N atributos
    def test_update_workstation_by_id_success(self, created_workstation, client):
        workstation_id = created_workstation["id"]
        update_payload = {
            "user": random_users_id(),
            "status": "INACTIVE", 
            "description": "description actualizada"
        }
        response = client.patch(f"/api/v1/workstations/{workstation_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "INACTIVE"
        assert data["description"] == "description actualizada"

    # prueba el endpoint de patch para actualizar un workstation con id inexistente, lanza error
    def test_update_workstation_by_id_not_found(self, client):
        response = client.patch("/api/v1/workstations/id-8382heds", json={"status": "INACTIVE"})
        assert response.status_code == 404

    # prueba el endpoint de patch para actualizar y ver si update_at es mayor
    def test_update_workstation_updates_updated_at(self, created_workstation, client):
        workstation_id = created_workstation["id"]
        original_updated_at = created_workstation["updated_at"]
        client.patch(f"/api/v1/workstations/{workstation_id}", json={"description": "Nueva descripcion"})
        response = client.get(f"/api/v1/workstations/{workstation_id}")
        new_updated_at = response.json()["updated_at"]
        # updated_at debe haber cambiado (o ser igual si es muy rápido — depende)
        assert new_updated_at >= original_updated_at

    # prueba el endpoint de patch al actualizar a un status que no existe
    def test_update_workstation_invalid_status(self, created_workstation, client):
        response = client.patch(f"/api/v1/workstations/{created_workstation['id']}", json={"status": "INVALID"})
        assert response.status_code == 422


class TestDeleteWorkstation:
    # prueba el endpoint de delete 
    def test_delete_workstation_by_id_success(self, workstation_payload, client):
        # crear workstation exclusivo para este test
        create_resp = client.post("/api/v1/workstations/", json=workstation_payload)
        workstation_id = create_resp.json()["id"]

        # eliminarlo segun el id
        delete_resp = client.delete(f"/api/v1/workstations/{workstation_id}")
        assert delete_resp.status_code == 204

        # verificar que ya no existe
        get_resp = client.get(f"/api/v1/workstations/{workstation_id}")
        assert get_resp.status_code == 404

    # prueba el endpoint de delete con un id inexistente
    def test_delete_workstation_by_id_not_found(self, client):
        response = client.delete("/api/v1/workstations/id-inexistente-jeje")
        assert response.status_code == 404

    # prueba el endpoint de delete 2 veces para ver si se elimino a la primera, si sale a la segunda tambien esta mal
    def test_delete_workstation_by_id_idempotent(self, workstation_payload, client):
        create_resp = client.post("/api/v1/workstations/", json=workstation_payload)
        workstation_id = create_resp.json()["id"]
        client.delete(f"/api/v1/workstations/{workstation_id}")
        second_delete = client.delete(f"/api/v1/workstations/{workstation_id}")
        assert second_delete.status_code == 404
