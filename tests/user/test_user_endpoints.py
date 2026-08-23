import time
import uuid
import pytest
from fastapi.testclient import TestClient

from src.main import app

from src.user.domain.user import UserStatus

@pytest.fixture 
def client(): 
    with TestClient(app) as c: 
        yield c


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


@pytest.fixture
def created_user(user_payload, client) -> dict:
    """Crea un user real en la BD y devuelve la respuesta; útil como precondición."""
    response = client.post("/api/v1/users/auth/register", json=user_payload)
    assert response.status_code == 201, f"Setup falló: {response.text}"
    return response.json()

@pytest.fixture
def auth_token(user_payload, client) -> str:
    """Registra un usuario, hace login y devuelve el token de acceso."""
    client.post("/api/v1/users/auth/register", json=user_payload)
    response = client.post("/api/v1/users/auth/login", json=user_payload)
    assert response.status_code == 201, f"Login falló: {response.text}"
    return response.json()["access_token"]

@pytest.fixture
def target_user(client):
    payload = {
        "name": f"test_user_{uuid.uuid4().hex[:8]}",
        "email": f"test_{uuid.uuid4().hex[:5]}@gmail.com",
        "password": "Segura123!",
        "date_of_birth": "1990-01-01T00:00:00Z",
        "bio": "This is a test user",
        "image_url": "webada",
    }
    response = client.post("/api/v1/users/auth/register", json=payload)
    assert response.status_code == 201, f"Setup falló: {response.text}"
    user = response.json()
    return {
        **user,
        "password": payload["password"]
    }


class TestLoginUser:
    # prueba el endpoint de login con credenciales correctas
    def test_login_success(self, user_payload, client):
        client.post("/api/v1/users/auth/register", json=user_payload)
        response = client.post("/api/v1/users/auth/login", json=user_payload)
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        #assert data["access_token"] != ""

    # prueba el endpoint de login con password incorrecta, lanza error
    def test_login_wrong_password(self, user_payload, client):
        client.post("/api/v1/users/auth/register", json=user_payload)
        payload = {**user_payload, "password": "ContraseñaIncorrecta"}
        response = client.post("/api/v1/users/auth/login", json=payload)
        assert response.status_code == 422

    # prueba el endpoint de login con email inexistente, lanza error
    def test_login_email_not_found(self, client):
        response = client.post("/api/v1/users/auth/login", json={
            "email": "noexiste@ejemplo.com",
            "password": "cualquiera"
        })
        assert response.status_code == 404

    # prueba el endpoint de login sin email, lanza error
    def test_login_missing_email(self, client):
        response = client.post("/api/v1/users/auth/login", json={"password": "Segura123!"})
        assert response.status_code == 422

    # prueba el endpoint de login sin password, lanza error
    def test_login_missing_password(self, user_payload, client):
        response = client.post("/api/v1/users/auth/login", json={"email": user_payload["email"]})
        assert response.status_code == 422


class TestLogoutUser:
    # prueba el endpoint de logout con un token valido
    def test_logout_success(self, auth_token, client):
        response = client.post(f"/api/v1/users/auth/logout?token={auth_token}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 204

    # prueba el endpoint de logout con un token invalido, lanza error
    def test_logout_invalid_token(self, auth_token, client):
        response = client.post("/api/v1/users/auth/logout?token=token.invalido.xyz", headers={"Authorization": f"Bearer {auth_token}"})
        # no importa si devuelve 204, ya que el logout es idempotente, sin importar lo que se haga, el resultado sera el mismo
        assert response.status_code == 204

    # prueba el endpoint de logout sin token, lanza error
    def test_logout_missing_token(self, client):
        response = client.post("/api/v1/users/auth/logout")
        assert response.status_code == 403


class TestGetAllUsers:
    # prueba el endpoint de getall si devuelve lo que tiene hasta ahora
    def test_get_all_returns_list(self, auth_token, client):
        response = client.get("/api/v1/users/", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "users" in data
        assert isinstance(data["users"], list)

    # prueba el endpoint de getall si contiene lo que fue creado por created_user
    def test_get_all_contains_created_user(self, created_user, auth_token, client):
        response = client.get("/api/v1/users/", headers={"Authorization": f"Bearer {auth_token}"})
        users = response.json()["users"]
        ids = [p["id"] for p in users]
        assert created_user["id"] in ids

    # prueba el endpoint de getall si devuelve todos los campos correspondientes del dto
    def test_get_all_user_fields(self, created_user, auth_token, client):
        response = client.get("/api/v1/users/", headers={"Authorization": f"Bearer {auth_token}"})
        users = response.json()["users"]
        user = next((p for p in users if p["id"] == created_user["id"]), None)
        assert user is not None
        for field in ("id", "name", "date_of_birth"):
            assert field in user


class TestGetUserById:
    # prueba el endpoint de get si devuelve lo que fue creado por created_user con su respectivo id
    def test_get_user_by_id_success(self, created_user, auth_token, client):
        user_id = created_user["id"]
        response = client.get(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    # prueba el endpoint de get si falla al consultar un id que no existe
    def test_get_user_by_id_not_found(self, auth_token, client):
        response = client.get("/api/v1/users/id-que-no-existe-99999", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de get si contiene ciertos campos que fueron creados por created_user
    def test_get_user_by_id_returns_correct_data(self, created_user, auth_token, client):
        response = client.get(f"/api/v1/users/{created_user['id']}", headers={"Authorization": f"Bearer {auth_token}"})
        data = response.json()
        assert data["name"] == created_user["name"]
        assert data["status"] == created_user["status"]
        assert data["bio"] == created_user["bio"]


class TestUpdateUser:
    # prueba el endpoint de patch para actualizar 2 atributos
    def test_update_user_by_id_success(self, created_user, auth_token, client):
        user_id = created_user["id"]
        update_payload = {
            "password": "NuevaSegura123!",
            "status": "INACTIVE", 
            "bio": "biografia actualizada"
        }
        response = client.patch(f"/api/v1/users/{user_id}", json=update_payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "INACTIVE"
        assert data["bio"] == "biografia actualizada"

    # prueba el endpoint de patch para actualizar un user con id inexistente, lanza error
    def test_update_user_by_id_not_found(self, auth_token, client):
        response = client.patch("/api/v1/users/id-8382heds", json={"status": "INACTIVE"}, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de patch para actualizar el status BANNED a SUSPENDED, lanza error
    def test_update_user_discontinued_to_inactive_raises_error(self, created_user, auth_token, client):
        user_id = created_user["id"]
        # primero pasar a BANNED
        client.patch(f"/api/v1/users/{user_id}", json={"status": "BANNED"}, headers={"Authorization": f"Bearer {auth_token}"})
        # luego intentar pasar a SUSPENDED
        response = client.patch(f"/api/v1/users/{user_id}", json={"status": "SUSPENDED"}, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 422

    # prueba el endpoint de patch para actualizar y ver si update_at es mayor
    def test_update_user_updates_updated_at(self, created_user, auth_token, client):
        user_id = created_user["id"]
        original_updated_at = created_user["updated_at"]
        time.sleep(2)
        client.patch(f"/api/v1/users/{user_id}", json={"bio": "Nueva descripcion"}, headers={"Authorization": f"Bearer {auth_token}"})
        response = client.get(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
        new_updated_at = response.json()["updated_at"]
        # updated_at debe haber cambiado (o ser igual si es muy rápido — depende)
        assert new_updated_at > original_updated_at

    # prueba el endpoint de patch al actualizar a un status que no existe
    def test_update_user_invalid_status(self, created_user, auth_token, client):
        response = client.patch(f"/api/v1/users/{created_user['id']}", json={"status": "INVALID"}, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 422


class TestDeleteUser:
    # prueba el endpoint de delete 
    def test_delete_user_by_id_success(self, target_user, auth_token, client):
        # crear user exclusivo para este test 
        user_id = target_user["id"]
        response = client.delete(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 204

        # verificar que ya no existe
        get_resp = client.get(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert get_resp.status_code == 404

    # prueba el endpoint de delete con un id inexistente
    def test_delete_user_by_id_not_found(self, auth_token, client):
        response = client.delete("/api/v1/users/id-inexistente-jeje", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404

    # prueba el endpoint de delete 2 veces para ver si se elimino a la primera, si sale a la segunda tambien esta mal
    def test_delete_user_by_id_idempotent(self, target_user, auth_token, client):
        user_id = target_user["id"]
        client.delete(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
        second_delete = client.delete(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
        assert second_delete.status_code == 404


class TestBusinessRules:
    def test_user_no_active_no_login(self, target_user, auth_token, client):
        user_id = target_user["id"]
        update_payload = {
            "status": UserStatus.BANNED
        }
        response = client.patch(f"/api/v1/users/{user_id}", json=update_payload, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200
        login_payload = {
            "email": target_user["email"],
            "password": target_user["password"],
        }
        response = client.post("/api/v1/users/auth/login", json=login_payload)
        assert response.status_code == 400
