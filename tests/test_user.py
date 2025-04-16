from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': "none@ex.com"})
    assert response.status_code == 404
    assert response.json() == {'detail': "User not found"}


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'email': 'abc@gmail.com',
        "password": "23131231",
        "name": "New User"
    }
    response = client.post("/api/v1/user", params=new_user)
    assert response.status_code == 201

    response_data = response.json()

    assert "email" in response_data
    assert response_data["email"] == new_user["email"]
    assert "name" in response_data
    assert response_data["name"] == new_user["name"]


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_user_email = users[0]['email']
    new_user = {
        "email": existing_user_email,
        "password": "anotherpassword123",
        "name": "Duplicate User"
    }

    response = client.post("/api/v1/user", json=new_user)

    # Проверяем конфликт (409 Conflict)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}


def test_delete_user():
    '''Удаление пользователя'''
    # test_user = {
    #     "email": "todelete@example.com",
    #     "password": "todelete123",
    #     "name": "To Be Deleted"
    # }
    # create_response = client.post("/api/v1/user", json=test_user)
    # assert create_response.status_code == 201

    # user_email = create_response.json()["email"]

    delete_response = client.delete(f"/api/v1/user", params={"email": users[0]['email']})

    assert delete_response.status_code == 204

    get_response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert get_response.status_code == 404
