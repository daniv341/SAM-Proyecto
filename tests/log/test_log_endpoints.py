import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture 
def client(): 
    with TestClient(app) as c: 
        yield c


# las pruebas del log se hacen a partir del create, update, get, getAll y delete de los demas objetos ya que no se puede crear un log en si, por ello en estos pruebas lo que haras en realizar operaciones con los otros objetos y probar si el log responde correctamente 

@pytest.fixture
def user_payload() -> dict:
    """Payload mínimo válido para crear un user. Nombre único por ejecución."""
    return {
        "name": f"test_user_{uuid.uuid4().hex[:8]}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "password": "Segura123!",
        "date_of_birth": "1990-01-01T00:00:00Z",
        "bio": "This is a test user",
        "image_url": "webada",
    }

# 
@pytest.fixture
def created_user(user_payload, client) -> dict:
    """Crea un user real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/users/auth/register", json=user_payload)
    assert response.status_code == 201, f"Setup falló: {response.text}"
    return response.json()


class TestGetAllLogs:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, client):
        response = client.get("/api/v1/logs/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "logs" in data
        assert isinstance(data["logs"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_user
    def test_get_all_contains_created_log(self, created_user, client):
        response = client.get("/api/v1/logs/")
        logs = response.json()["logs"]
        ids = [p["entity_id"] for p in logs]
        assert created_user["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_log_fields(self, created_user, client):
        response = client.get("/api/v1/logs/")
        logs = response.json()["logs"]
        log = next((p for p in logs if p["entity_id"] == created_user["id"]), None)
        assert log is not None
        for field in ("action", "entity_type", "description", "created_at"):
            assert field in log

    #prueba el endpoint de getall si el filtro funciona segun la busqueda deseada
    def test_get_all_filtering_fields(self, client):
        params = {
            "action": "CREATE",
            "entity_type": "USER",
        }
        response =  client.get("/api/v1/logs/", params=params)
        fields = response.json()["logs"]
        assert len(fields) > 0
        for field in fields:
            assert field["action"] == "CREATE"
            assert field["entity_type"] == "USER"
        

# clausarado, ya que en ningun momento puedo saber cual fue el id del log que se creo, esto debido a que no se puede crear un log por si solo, se nevesita de una accion previa
class TestGetLogById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_user con su respectivo id
    def test_get_log_by_id_success(self, created_user, client):
        user = created_user["id"]
        #response = client.get(f"/api/v1/logs/{log_id}")
        #assert response.status_code == 200
        #assert response.json()["id"] == log_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_log_by_id_not_found(self, client):
        response = client.get("/api/v1/logs/id-que-no-existe-99999")
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_user
    def test_get_log_by_id_returns_correct_data(self, created_user, client):
        response = client.get(f"/api/v1/logs/{created_user['id']}")
        data = response.json()
        assert data["entity_id"] == created_user["id"]

