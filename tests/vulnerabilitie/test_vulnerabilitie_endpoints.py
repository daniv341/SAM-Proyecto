import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

@pytest.fixture 
def client(): 
    with TestClient(app) as c: 
        yield c


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
def created_vulnerabilitie(vulnerabilitie_payload, client) -> dict:
    """Crea un user real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload)
    assert response.status_code == 201, f"Setup falló: {response.text}"
    return response.json()


class TestCreateVulnerabilitie:
    # prueba el endpoint de post con todos los atributos
    def test_create_vulnerabilitie_success(self, vulnerabilitie_payload, client):
        response = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["cve"] == vulnerabilitie_payload["cve"]
        assert data["severity"] == "LOW"
        assert "id" in data

    # prueba el endpoint de post sin los atributos opcionales
    def test_create_vulnerabilitie_without_optional_fields(self, client):
        payload = {
        "cve": "CVE-2026152",
        "severity": "MEDIUM",
        "url": "asffefwreg",
        "mitigation": False,
    }
        response = client.post("/api/v1/vulnerabilities/", json=payload)
        assert response.status_code == 201
        data = response.json()
        print(data)
        assert data["severity"] == "MEDIUM"
        assert data["cve"] == payload["cve"]

    # prueba el endpoint de post sin el name, lanza error
    def test_create_vulnerabilitie_missing_required_field(self, vulnerabilitie_payload, client):
        payload = vulnerabilitie_payload.copy()
        del payload["cve"]
        response = client.post("/api/v1/vulnerabilities/", json=payload)
        assert response.status_code == 422   # Unprocessable Entity

    # prueba el endpoint de post con cve vacio, lanza error
    def test_create_vulnerabilitie_empty_severity(self, vulnerabilitie_payload, client):
        payload = {**vulnerabilitie_payload, "cve": ""}
        response = client.post("/api/v1/vulnerabilities/", json=payload)
        assert response.status_code == 422

    # prueba el endpoint de post si devuelve created_at y updated_at
    def test_create_vulnerabilitie_returns_timestamps(self, client):
        payload = {
            "cve": "CVE-2026152",
            "description": "hola que hace",
            "severity": "LOW",
            "url": "asffefwreg",
            "mitigation": False,
        }
        response = client.post("/api/v1/vulnerabilities/", json=payload)
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllVulnerabilities:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, client):
        response = client.get("/api/v1/vulnerabilities/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "vulnerabilities" in data
        assert isinstance(data["vulnerabilities"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_vulnerabilitie
    def test_get_all_contains_created_vulnerabilitie(self, created_vulnerabilitie, client):
        response = client.get("/api/v1/vulnerabilities/")
        vulnerabilities = response.json()["vulnerabilities"]
        ids = [p["id"] for p in vulnerabilities]
        assert created_vulnerabilitie["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_vulnerabilitie_fields(self, created_vulnerabilitie, client):
        response = client.get("/api/v1/vulnerabilities/")
        vulnerabilities = response.json()["vulnerabilities"]
        print(response.json())
        vulnerabilitie = next((p for p in vulnerabilities if p["id"] == created_vulnerabilitie["id"]), None)
        assert vulnerabilitie is not None
        for field in ("cve", "severity", "mitigation"):
            assert field in vulnerabilitie


class TestGetVulnerabilitieById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_vulnerabilitie con su respectivo id
    def test_get_vulnerabilitie_by_id_success(self, created_vulnerabilitie, client):
        vulnerabilitie_id = created_vulnerabilitie["id"]
        response = client.get(f"/api/v1/vulnerabilities/{vulnerabilitie_id}")
        assert response.status_code == 200
        assert response.json()["id"] == vulnerabilitie_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_vulnerabilitie_by_id_not_found(self, client):
        response = client.get("/api/v1/vulnerabilities/id-que-no-existe-99999")
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_vulnerabilitie
    def test_get_vulnerabilitie_by_id_returns_correct_data(self, created_vulnerabilitie, client):
        response = client.get(f"/api/v1/vulnerabilities/{created_vulnerabilitie['id']}")
        data = response.json()
        assert data["cve"] == created_vulnerabilitie["cve"]


class TestUpdateVulnerabilitie:
# prueba el endpoint de patch para actualizar N atributos
    def test_update_vulnerabilitie_by_id_success(self, created_vulnerabilitie, client):
        vulnerabilitie_id = created_vulnerabilitie["id"]
        update_payload = {
            "description": "description actualizada", 
            "mitigation": True
        }
        response = client.patch(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "description actualizada"
        assert data["mitigation"] == True

    # prueba el endpoint de patch para actualizar un vulnerabilitie con id inexistente, lanza error
    def test_update_vulnerabilitie_by_id_not_found(self, client):
        response = client.patch("/api/v1/vulnerabilities/id-8382heds", json={"severity": "MEDIUM"})
        assert response.status_code == 404

    # prueba el endpoint de patch para actualizar y ver si update_at es mayor
    def test_update_vulnerabilitie_updates_updated_at(self, created_vulnerabilitie, client):
        vulnerabilitie_id = created_vulnerabilitie["id"]
        original_updated_at = created_vulnerabilitie["updated_at"]
        client.patch(f"/api/v1/vulnerabilities/{vulnerabilitie_id}", json={"description": "Nueva descripcion"})
        response = client.get(f"/api/v1/vulnerabilities/{vulnerabilitie_id}")
        new_updated_at = response.json()["updated_at"]
        # updated_at debe haber cambiado (o ser igual si es muy rápido — depende)
        assert new_updated_at >= original_updated_at


class TestDeleteVulnerabilitie:
    # prueba el endpoint de delete 
    def test_delete_vulnerabilitie_by_id_success(self, vulnerabilitie_payload, client):
        # crear vulnerabilitie exclusivo para este test
        create_resp = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload)
        vulnerabilitie_id = create_resp.json()["id"]

        # eliminarlo segun el id
        delete_resp = client.delete(f"/api/v1/vulnerabilities/{vulnerabilitie_id}")
        assert delete_resp.status_code == 204

        # verificar que ya no existe
        get_resp = client.get(f"/api/v1/vulnerabilities/{vulnerabilitie_id}")
        assert get_resp.status_code == 404

    # prueba el endpoint de delete con un id inexistente
    def test_delete_vulnerabilitie_by_id_not_found(self, client):
        response = client.delete("/api/v1/vulnerabilities/id-inexistente-jeje")
        assert response.status_code == 404

    # prueba el endpoint de delete 2 veces para ver si se elimino a la primera, si sale a la segunda tambien esta mal
    def test_delete_vulnerabilitie_by_id_idempotent(self, vulnerabilitie_payload, client):
        create_resp = client.post("/api/v1/vulnerabilities/", json=vulnerabilitie_payload)
        vulnerabilitie_id = create_resp.json()["id"]
        client.delete(f"/api/v1/vulnerabilities/{vulnerabilitie_id}")
        second_delete = client.delete(f"/api/v1/vulnerabilities/{vulnerabilitie_id}")
        assert second_delete.status_code == 404
