import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

@pytest.fixture 
def client(): 
    with TestClient(app) as c: 
        yield c


@pytest.fixture
def user_payload() -> dict:
    """Payload mínimo válido para crear un user. Nombre único por ejecución."""
    return {
        "name": f"test_user_{uuid.uuid4().hex[:8]}",
        "date_of_birth": "1990-01-01T00:00:00Z",
        "bio": "This is a test user",
        "image_url": "webada",
    }


@pytest.fixture
def created_user(user_payload, client) -> dict:
    """Crea un user real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/users/", json=user_payload)
    assert response.status_code == 201, f"Setup falló: {response.text}"
    return response.json()


class TestCreateUser:
    # prueba el endpoint de post con todos los atributos
    def test_create_user_success(self, user_payload: dict, client):
        response = client.post("/api/v1/users/", json=user_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == user_payload["name"]
        assert data["status"] == "ACTIVE"
        assert "id" in data

    # prueba el endpoint de post sin los atributos opcionales
    def test_create_user_without_optional_fields(self, client):
        payload = {
            "name": f"test_user_{uuid.uuid4().hex[:8]}",
            "date_of_birth": "1990-01-01T00:00:00Z",
        }
        response = client.post("/api/v1/users/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "ACTIVE"
        assert data["name"] == payload["name"]

    # prueba el endpoint de post sin el name, lanza error
    def test_create_user_missing_required_field(self, user_payload, client):
        payload = user_payload.copy()
        del payload["name"]
        response = client.post("/api/v1/users/", json=payload)
        assert response.status_code == 422   # Unprocessable Entity
    
    # prueba el endpoint de post con date_of_birth invalido, lanza error
    def test_create_user_invalid_date_format(self, user_payload, client):
        payload = {**user_payload, "date_of_birth": "no-es-una-fecha"}
        response = client.post("/api/v1/users/", json=payload)
        assert response.status_code == 422
    
    # prueba el endpoint de post con name vacio, lanza error
    def test_create_user_empty_name(self, user_payload, client):
        payload = {**user_payload, "name": ""}
        response = client.post("/api/v1/users/", json=payload)
        assert response.status_code == 422
    
    # prueba el endpoint de post si devuelve created_at y updated_at
    def test_create_user_returns_timestamps(self, client):
        payload = {
            "name": f"test_user_{uuid.uuid4().hex[:8]}",
            "date_of_birth": "1990-01-01T00:00:00Z",
            "bio": "This is a test user.",
            "image_url": "webada",
        }
        response = client.post("/api/v1/users/", json=payload)
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestGetAllUsers:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, client):
        response = client.get("/api/v1/users/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "users" in data
        assert isinstance(data["users"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_user
    def test_get_all_contains_created_user(self, created_user, client):
        response = client.get("/api/v1/users/")
        users = response.json()["users"]
        ids = [p["id"] for p in users]
        assert created_user["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_user_fields(self, created_user, client):
        response = client.get("/api/v1/users/")
        users = response.json()["users"]
        print(response.json())
        user = next((p for p in users if p["id"] == created_user["id"]), None)
        assert user is not None
        for field in ("id", "name", "date_of_birth"):
            assert field in user


class TestGetUserById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_user con su respectivo id
    def test_get_user_by_id_success(self, created_user, client):
        user_id = created_user["id"]
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_user_by_id_not_found(self, client):
        response = client.get("/api/v1/users/id-que-no-existe-99999")
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_user
    def test_get_user_by_id_returns_correct_data(self, created_user, client):
        response = client.get(f"/api/v1/users/{created_user['id']}")
        data = response.json()
        assert data["name"] == created_user["name"]
        assert data["status"] == created_user["status"]
        assert data["bio"] == created_user["bio"]


class TestUpdateUser:
    # prueba el endpoint de patch para actualizar 2 atributos
    def test_update_user_by_id_success(self, created_user, client):
        user_id = created_user["id"]
        update_payload = {
            "status": "INACTIVE", 
            "bio": "biografia actualizada"
        }
        response = client.patch(f"/api/v1/users/{user_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "INACTIVE"
        assert data["bio"] == "biografia actualizada"

    # prueba el endpoint de patch para actualizar un user con id inexistente, lanza error
    def test_update_user_by_id_not_found(self, client):
        response = client.patch("/api/v1/users/id-8382heds", json={"status": "INACTIVE"})
        assert response.status_code == 404

    # prueba el endpoint de patch para actualizar el status BANNED a SUSPENDED, lanza error
    def test_update_user_discontinued_to_inactive_raises_error(self, created_user, client):
        user_id = created_user["id"]
        # primero pasar a BANNED
        client.patch(f"/api/v1/users/{user_id}", json={"status": "BANNED"})
        # luego intentar pasar a SUSPENDED
        response = client.patch(f"/api/v1/users/{user_id}", json={"status": "SUSPENDED"})
        assert response.status_code == 422

    # prueba el endpoint de patch para actualizar y ver si update_at es mayor
    def test_update_user_updates_updated_at(self, created_user, client):
        user_id = created_user["id"]
        original_updated_at = created_user["updated_at"]
        client.patch(f"/api/v1/users/{user_id}", json={"bio": "Nueva descripcion"})
        response = client.get(f"/api/v1/users/{user_id}")
        new_updated_at = response.json()["updated_at"]
        # updated_at debe haber cambiado (o ser igual si es muy rápido — depende)
        assert new_updated_at >= original_updated_at

    # prueba el endpoint de patch al actualizar a un status que no existe
    def test_update_user_invalid_status(self, created_user, client):
        response = client.patch(f"/api/v1/users/{created_user['id']}", json={"status": "INVALID"})
        assert response.status_code == 422


class TestDeleteUser:
    # prueba el endpoint de delete 
    def test_delete_user_by_id_success(self, user_payload, client):
        # crear user exclusivo para este test
        create_resp = client.post("/api/v1/users/", json=user_payload)
        user_id = create_resp.json()["id"]

        # eliminarlo segun el id
        delete_resp = client.delete(f"/api/v1/users/{user_id}")
        assert delete_resp.status_code == 204

        # verificar que ya no existe
        get_resp = client.get(f"/api/v1/users/{user_id}")
        assert get_resp.status_code == 404

    # prueba el endpoint de delete con un id inexistente
    def test_delete_user_by_id_not_found(self, client):
        response = client.delete("/api/v1/users/id-inexistente-jeje")
        assert response.status_code == 404

    # prueba el endpoint de delete 2 veces para ver si se elimino a la primera, si sale a la segunda tambien esta mal
    def test_delete_user_by_id_idempotent(self, user_payload, client):
        create_resp = client.post("/api/v1/users/", json=user_payload)
        user_id = create_resp.json()["id"]
        client.delete(f"/api/v1/users/{user_id}")
        second_delete = client.delete(f"/api/v1/users/{user_id}")
        assert second_delete.status_code == 404
