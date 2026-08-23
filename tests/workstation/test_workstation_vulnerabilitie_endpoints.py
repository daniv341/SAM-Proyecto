import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

WORKSTATION_IDS = [
"01M0NWV11Q7APEVHQ0VZ74SR7W",
"01M0NWV1TY7FZSGVE01HQW2N2N",
"01M0NWV3EXAP14RC3C2K344GS7",
"01M0NWV56HKZ93P35JDF02EFN6",
"01M0NWV665RNCMG488ZV8G73HM",
]

VULNERABILITIE_IDS = [
"01M0313Y8SXE1CBTMPYQZ4YESH",
"01M0313YD806984NQ71H45SYMZ",
"01M0313YHH0N18HCXV783R07DK",
]

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

class TestAddvulnerabilitieToWorkstation:
    # prueba el endpoint de post para añadir una vulnerabilidad a un workstation
    def test_add_vulnerabilitie_to_workstation_success(self, auth_token, client):
        workstation_id = WORKSTATION_IDS[1]
        vulnerabilitie_id = VULNERABILITIE_IDS[1]
        response = client.post(f"/api/v1/workstations/{workstation_id}/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 204

    # prueba el endpoint de post al intentar añadir una vulnerabilidad a un workstation que no existe
    def test_add_vulnerabilitie_to_workstation_not_found(self, auth_token, client):
        response = client.post(f"/api/v1/workstations/id-workstation-inexistente/vulnerabilities/{VULNERABILITIE_IDS[1]}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de post al intentar añadir una vulnerabilidad que no existe
    def test_add_vulnerabilitie_not_found(self, auth_token, client):
        response = client.post(f"/api/v1/workstations/{WORKSTATION_IDS[1]}/vulnerabilities/id-vulnerabilitie-inexistente", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de post al intentar añadir dos veces la misma vulnerabilidad
    def test_add_vulnerabilitie_duplicate(self, auth_token, client):
        workstation_id = WORKSTATION_IDS[2]
        vulnerabilitie_id = VULNERABILITIE_IDS[2]
        first_response = client.post(f"/api/v1/workstations/{workstation_id}/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert first_response.status_code == 204
        second_response = client.post(f"/api/v1/workstations/{workstation_id}/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert second_response.status_code == 422


class TestRemovevulnerabilitieFromWorkstation:
    # prueba el endpoint de delete para eliminar una vulnerabilidad de un workstation
    def test_remove_vulnerabilitie_from_workstation_success(self, auth_token, client):
        workstation_id = WORKSTATION_IDS[1]
        vulnerabilitie_id = VULNERABILITIE_IDS[1]
        response = client.delete(f"/api/v1/workstations/{workstation_id}/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 204

    # prueba el endpoint de delete con un workstation inexistente
    def test_remove_vulnerabilitie_workstation_not_found(self, auth_token, client):
        response = client.delete(f"/api/v1/workstations/id-workstation-inexistente/vulnerabilities/{VULNERABILITIE_IDS[2]}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de delete con una vulnerabilidad inexistente
    def test_remove_vulnerabilitie_not_found(self, auth_token, client):
        response = client.delete(f"/api/v1/workstations/{WORKSTATION_IDS[3]}/vulnerabilities/id-vulnerabilitie-inexistente", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de delete al intentar eliminar una relacion que no existe
    def test_remove_vulnerabilitie_relationship_not_found(self, auth_token, client):
        response = client.delete(f"/api/v1/workstations/{WORKSTATION_IDS[4]}/vulnerabilities/{VULNERABILITIE_IDS[2]}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404


class TestGetWorkstationVulnerabilities:
    # prueba el endpoint de get si devuelve una lista de vulnerabilidades
    def test_get_workstation_vulnerabilities_returns_list(self, auth_token, client):
        response = client.get(f"/api/v1/workstations/{WORKSTATION_IDS[1]}/vulnerabilities", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    # prueba el endpoint de get si contiene la vulnerabilidad asociada
    def test_get_workstation_vulnerabilities_contains_vulnerabilitie(self, auth_token, client):
        workstation_id = WORKSTATION_IDS[4]
        vulnerabilitie_id = VULNERABILITIE_IDS[1]
        add_response = client.post(f"/api/v1/workstations/{workstation_id}/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert add_response.status_code == 204
        response = client.get(f"/api/v1/workstations/{workstation_id}/vulnerabilities", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        vulnerabilities = response.json()
        ids = [v["id"] for v in vulnerabilities]
        assert vulnerabilitie_id in ids

    # prueba el endpoint de get con un workstation inexistente
    def test_get_workstation_vulnerabilities_workstation_not_found(self, auth_token, client):
        response = client.get("/api/v1/workstations/id-workstation-inexistente/vulnerabilities", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de get si devuelve los campos correspondientes del dto
    def test_get_workstation_vulnerabilities_returns_correct_fields(self, auth_token, client):
        workstation_id = WORKSTATION_IDS[3]
        vulnerabilitie_id = VULNERABILITIE_IDS[2]
        add_response = client.post(f"/api/v1/workstations/{workstation_id}/vulnerabilities/{vulnerabilitie_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert add_response.status_code == 204
        response = client.get(f"/api/v1/workstations/{workstation_id}/vulnerabilities", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        vulnerabilities = response.json()
        vulnerabilitie = next((v for v in vulnerabilities if v["id"] == vulnerabilitie_id), None)
        assert vulnerabilitie is not None
        for field in ("id", "cve"):
            assert field in vulnerabilitie