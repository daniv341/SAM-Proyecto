import random
import time
import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

USER_IDS = [
"01M0NVBADDP9X5086JTHSFYR5M",
"01M0NVBB68WSZ3F28A8858NV9E",
"01M0NVBBYGRM1K5PGER527TA7F",
"01M0NVBCT3K26BRPDAA2CQZWP5",
"01M0NVBDJ70JYB2GSSRJ4SN4VW",
"01M0NVBEE5394C45A8X895SQ5X",
"01M0NVBFDWQP1QNRAZRQ6F89DP",
"01M0NVBGDS5YAE3G2VW6VS56WW",
"01M0NVBHDXJH85SZTARW929F2G",
"01M0NVBJ9ERNHS0V8QM41XW26C",
]

def random_users_id() -> str:
    return random.choice(USER_IDS)

@pytest.fixture 
def client(): 
    with TestClient(app) as c: 
        yield c


@pytest.fixture
def auth_token(client) -> str:
    """Registra un usuario, hace login y devuelve el token de acceso."""
    user_payload = {
        "name": f"test_user_{uuid.uuid4().hex[:8]}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "password": "Segura123!",
        "date_of_birth": "1990-01-01T00:00:00Z"
    }
    client.post("/api/v1/users/auth/register", json=user_payload)
    response = client.post("/api/v1/users/auth/login", json=user_payload)
    assert response.status_code == 201, f"Login falló: {response.text}"
    return response.json()["access_token"]

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
def created_workstation(workstation_payload, auth_token, client) -> dict:
    """Crea un workstation real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/workstations/", json=workstation_payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201, f"Setup falló: {response.text}"
    return response.json()


class TestCreateWorkstation:
    # prueba el endpoint de post con todos los atributos
    def test_create_workstation_success(self, workstation_payload, auth_token,client):
        response = client.post("/api/v1/workstations/", json=workstation_payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == workstation_payload["description"]
        assert data["status"] == "ACTIVE"
        assert "id" in data

    # prueba el endpoint de post sin los atributos opcionales
    def test_create_workstation_without_optional_fields(self, auth_token,client):
        payload = {
            "user": random_users_id(),
            "type": "DESKTOP",
            "area": "SUPPORT",
        }
        response = client.post("/api/v1/workstations/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "ACTIVE"
        assert data["type"] == payload["type"]

    # prueba el endpoint de post sin el user, lanza error
    def test_create_workstation_missing_required_field(self, workstation_payload, auth_token, client):
        payload = workstation_payload.copy()
        del payload["user"]
        response = client.post("/api/v1/workstations/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 422   # Unprocessable Entity

    # prueba el endpoint de post si devuelve created_at y updated_at
    def test_create_workstation_returns_timestamps(self, auth_token,client):
        payload = {
            "user": random_users_id(),
            "description": "descripcion de prueba",
            "type": "DESKTOP",
            "area": "SUPPORT"
        }
        response = client.post("/api/v1/workstations/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllWorkstations:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, auth_token, client):
        response = client.get("/api/v1/workstations/", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "workstations" in data
        assert isinstance(data["workstations"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_workstation
    def test_get_all_contains_created_workstation(self, created_workstation, auth_token, client):
        response = client.get("/api/v1/workstations/", headers={"Authorization": f"Bearer {auth_token}"})
        workstations = response.json()["workstations"]
        ids = [p["id"] for p in workstations]
        assert created_workstation["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_workstation_fields(self, created_workstation, auth_token, client):
        response = client.get("/api/v1/workstations/", headers={"Authorization": f"Bearer {auth_token}"})
        workstations = response.json()["workstations"]
        workstation = next((p for p in workstations if p["id"] == created_workstation["id"]), None)
        assert workstation is not None
        for field in ("id", "status", "type"):
            assert field in workstation

    #prueba el endpoint de getall si el filtro funciona segun la busqueda deseada
    def test_get_all_filtering_fields(self, auth_token, client):
        params = {
            "status": "ACTIVE",
            "type": "DESKTOP",
        }
        response =  client.get("/api/v1/workstations/", params=params, headers={"Authorization": f"Bearer {auth_token}"})
        fields = response.json()["workstations"]
        assert len(fields) > 0
        for field in fields:
            assert field["status"] == "ACTIVE"
            assert field["type"] == "DESKTOP"

class TestGetWorkstationById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_workstation con su respectivo id
    def test_get_workstation_by_id_success(self, created_workstation, auth_token, client):
        workstation_id = created_workstation["id"]
        response = client.get(f"/api/v1/workstations/{workstation_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        assert response.json()["id"] == workstation_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_workstation_by_id_not_found(self, auth_token, client):
        response = client.get("/api/v1/workstations/id-que-no-existe-99999", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_workstation
    def test_get_workstation_by_id_returns_correct_data(self, created_workstation, auth_token, client):
        response = client.get(f"/api/v1/workstations/{created_workstation['id']}", headers={"Authorization": f"Bearer {auth_token}"})
        data = response.json()
        assert data["description"] == created_workstation["description"]


class TestUpdateWorkstation:
# prueba el endpoint de patch para actualizar N atributos
    def test_update_workstation_by_id_success(self, created_workstation, auth_token, client):
        workstation_id = created_workstation["id"]
        update_payload = {
            "user": random_users_id(),
            "status": "BANNED", 
            "description": "description actualizada"
        }
        response = client.patch(f"/api/v1/workstations/{workstation_id}", json=update_payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BANNED"
        assert data["description"] == "description actualizada"

    # prueba el endpoint de patch para actualizar un workstation con id inexistente, lanza error
    def test_update_workstation_by_id_not_found(self, auth_token, client):
        response = client.patch("/api/v1/workstations/id-8382heds", json={"status": "INACTIVE"}, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de patch para actualizar y ver si update_at es mayor
    def test_update_workstation_updates_updated_at(self, created_workstation, auth_token, client):
        workstation_id = created_workstation["id"]
        original_updated_at = created_workstation["updated_at"]
        time.sleep(2)
        client.patch(f"/api/v1/workstations/{workstation_id}", json={"description": "Nueva descripcion"}, headers={"Authorization": f"Bearer {auth_token}"})
        response = client.get(f"/api/v1/workstations/{workstation_id}", headers={"Authorization": f"Bearer {auth_token}"})
        new_updated_at = response.json()["updated_at"]
        # updated_at debe haber cambiado (o ser igual si es muy rápido — depende)
        assert new_updated_at > original_updated_at

    # prueba el endpoint de patch al actualizar a un status que no existe
    def test_update_workstation_invalid_status(self, created_workstation, auth_token, client):
        response = client.patch(f"/api/v1/workstations/{created_workstation['id']}", json={"status": "INVALID"}, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 422


class TestDeleteWorkstation:
    # prueba el endpoint de delete 
    def test_delete_workstation_by_id_success(self, workstation_payload, auth_token, client):
        # crear workstation exclusivo para este test
        response = client.post("/api/v1/workstations/", json=workstation_payload, headers={"Authorization": f"Bearer {auth_token}"})
        workstation_id = response.json()["id"]

        # eliminarlo segun el id
        delete_resp = client.delete(f"/api/v1/workstations/{workstation_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert delete_resp.status_code == 204

        # verificar que ya no existe
        get_resp = client.get(f"/api/v1/workstations/{workstation_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert get_resp.status_code == 404

    # prueba el endpoint de delete con un id inexistente
    def test_delete_workstation_by_id_not_found(self, auth_token, client):
        response = client.delete("/api/v1/workstations/id-inexistente-jeje", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de delete 2 veces para ver si se elimino a la primera, si sale a la segunda tambien esta mal
    def test_delete_workstation_by_id_idempotent(self, workstation_payload, auth_token, client):
        response = client.post("/api/v1/workstations/", json=workstation_payload, headers={"Authorization": f"Bearer {auth_token}"})
        workstation_id = response.json()["id"]
        client.delete(f"/api/v1/workstations/{workstation_id}", headers={"Authorization": f"Bearer {auth_token}"})
        second_delete = client.delete(f"/api/v1/workstations/{workstation_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert second_delete.status_code == 404

