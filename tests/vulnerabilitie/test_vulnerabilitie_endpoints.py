import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

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
def vulnerabilitie_payload() -> dict:
    """Payload mínimo válido para crear un vulnerabilitie."""
    return {
        "cve": "CVE-2026152",
        "description": "hola que hace",
        "severity": "LOW",
        "url": "asffefwreg",
        "mitigation": False,
    }


@pytest.fixture
def created_vulnerabilitie(vulnerabilitie_payload, auth_token, client) -> dict:
    """Crea un user real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201, f"Setup falló: {response.text}"
    return response.json()


class TestCreateVulnerabilitie:
    # prueba el endpoint de post con todos los atributos
    def test_create_vulnerabilitie_success(self, vulnerabilitie_payload, auth_token, client):
        response = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 201
        data = response.json()
        assert data["cve"] == vulnerabilitie_payload["cve"]
        assert data["severity"] == "LOW"
        assert "id" in data

    # prueba el endpoint de post sin los atributos opcionales
    def test_create_vulnerabilitie_without_optional_fields(self, auth_token, client):
        payload = {
        "cve": "CVE-2026152",
        "severity": "MEDIUM",
        "url": "asffefwreg",
        "mitigation": False,
    }
        response = client.post("/api/v1/vulnerabilities/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 201
        data = response.json()
        assert data["severity"] == "MEDIUM"
        assert data["cve"] == payload["cve"]

    # prueba el endpoint de post sin el name, lanza error
    def test_create_vulnerabilitie_missing_required_field(self, vulnerabilitie_payload, auth_token, client):
        payload = vulnerabilitie_payload.copy()
        del payload["cve"]
        response = client.post("/api/v1/vulnerabilities/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 422   # Unprocessable Entity

    # prueba el endpoint de post con cve vacio, lanza error
    def test_create_vulnerabilitie_empty_severity(self, vulnerabilitie_payload, auth_token, client):
        payload = {**vulnerabilitie_payload, "cve": ""}
        response = client.post("/api/v1/vulnerabilities/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 422

    # prueba el endpoint de post si devuelve created_at y updated_at
    def test_create_vulnerabilitie_returns_timestamps(self, auth_token, client):
        payload = {
            "cve": "CVE-2026152",
            "description": "hola que hace",
            "severity": "LOW",
            "url": "asffefwreg",
            "mitigation": False,
        }
        response = client.post("/api/v1/vulnerabilities/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllVulnerabilities:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, auth_token, client):
        response = client.get("/api/v1/vulnerabilities/", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "vulnerabilities" in data
        assert isinstance(data["vulnerabilities"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_vulnerabilitie
    def test_get_all_contains_created_vulnerabilitie(self, created_vulnerabilitie, auth_token, client):
        response = client.get("/api/v1/vulnerabilities/", headers={"Authorization": f"Bearer {auth_token}"})
        vulnerabilities = response.json()["vulnerabilities"]
        ids = [p["id"] for p in vulnerabilities]
        assert created_vulnerabilitie["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_vulnerabilitie_fields(self, created_vulnerabilitie, auth_token, client):
        response = client.get("/api/v1/vulnerabilities/", headers={"Authorization": f"Bearer {auth_token}"})
        vulnerabilities = response.json()["vulnerabilities"]
        vulnerabilitie = next((p for p in vulnerabilities if p["id"] == created_vulnerabilitie["id"]), None)
        assert vulnerabilitie is not None
        for field in ("cve", "severity", "mitigation"):
            assert field in vulnerabilitie


class TestGetVulnerabilitieById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_vulnerabilitie con su respectivo id
    def test_get_vulnerabilitie_by_id_success(self, created_vulnerabilitie, auth_token, client):
        vulnerabilitie_id = created_vulnerabilitie["id"]
        response = client.get(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        assert response.json()["id"] == vulnerabilitie_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_vulnerabilitie_by_id_not_found(self, auth_token, client):
        response = client.get("/api/v1/vulnerabilities/id-que-no-existe-99999", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_vulnerabilitie
    def test_get_vulnerabilitie_by_id_returns_correct_data(self, created_vulnerabilitie, auth_token, client):
        response = client.get(f"/api/v1/vulnerabilities/{created_vulnerabilitie['id']}", headers={"Authorization": f"Bearer {auth_token}"})
        data = response.json()
        assert data["cve"] == created_vulnerabilitie["cve"]


class TestUpdateVulnerabilitie:
# prueba el endpoint de patch para actualizar N atributos
    def test_update_vulnerabilitie_by_id_success(self, created_vulnerabilitie, auth_token, client):
        vulnerabilitie_id = created_vulnerabilitie["id"]
        update_payload = {
            "description": "description actualizada", 
            "mitigation": True
        }
        response = client.patch(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", json=update_payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "description actualizada"
        assert data["mitigation"] == True

    # prueba el endpoint de patch para actualizar un vulnerabilitie con id inexistente, lanza error
    def test_update_vulnerabilitie_by_id_not_found(self, auth_token, client):
        response = client.patch("/api/v1/vulnerabilities/id-8382heds", json={"severity": "MEDIUM"}, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de patch para actualizar y ver si update_at es mayor
    def test_update_vulnerabilitie_updates_updated_at(self, created_vulnerabilitie, auth_token, client):
        vulnerabilitie_id = created_vulnerabilitie["id"]
        original_updated_at = created_vulnerabilitie["updated_at"]
        client.patch(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", json={"description": "Nueva descripcion"}, headers={"Authorization": f"Bearer {auth_token}"})
        response = client.get(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        new_updated_at = response.json()["updated_at"]
        # updated_at debe haber cambiado (o ser igual si es muy rápido — depende)
        assert new_updated_at >= original_updated_at


class TestDeleteVulnerabilitie:
    # prueba el endpoint de delete 
    def test_delete_vulnerabilitie_by_id_success(self, vulnerabilitie_payload, auth_token, client):
        # crear vulnerabilitie exclusivo para este test
        response = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload, headers={"Authorization": f"Bearer {auth_token}"})
        vulnerabilitie_id = response.json()["id"]

        # eliminarlo segun el id
        delete_resp = client.delete(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert delete_resp.status_code == 204

        # verificar que ya no existe
        get_resp = client.get(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert get_resp.status_code == 404

    # prueba el endpoint de delete con un id inexistente
    def test_delete_vulnerabilitie_by_id_not_found(self, auth_token, client):
        response = client.delete("/api/v1/vulnerabilities/id-inexistente-jeje", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de delete 2 veces para ver si se elimino a la primera, si sale a la segunda tambien esta mal
    def test_delete_vulnerabilitie_by_id_idempotent(self, vulnerabilitie_payload, auth_token, client):
        response = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload, headers={"Authorization": f"Bearer {auth_token}"})
        vulnerabilitie_id = response.json()["id"]
        client.delete(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        second_delete = client.delete(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert second_delete.status_code == 404
