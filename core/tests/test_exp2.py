import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from home.models import Car


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", email="test@example.com", password="password123")

@pytest.fixture
def token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token

@pytest.fixture
def authenticated_client(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client

@pytest.fixture
def car():
    return Car.objects.create(
        model="Toyota Corolla",
        year=2020,
        registration_number="ABC123",
        seating_capacity=5
    )
@pytest.mark.django_db
def test_registration(api_client):
    url = reverse('register')
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword123",
        "role": "user"
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data["message"] == "Registration successfully"
@pytest.mark.django_db
def test_login(api_client, user):
    url = reverse('login')
    data = {
        "email": user.email,
        "password": "password123"
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "token" in response.data
@pytest.mark.django_db
def test_add_car(authenticated_client):
    url = reverse('addCar')
    data = {
        "model": "Honda Civic",
        "year": 2019,
        "registration_number": "XYZ789",
        "seating_capacity": 5
    }
    response = authenticated_client.post(url, data)
    assert response.status_code == 201
    assert response.data["message"] == "Car added successfully"
@pytest.mark.django_db
def test_view_car(authenticated_client, car):
    url = reverse('car-detail', args=[car.id])
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data["model"] == car.model
@pytest.mark.django_db
def test_update_car(authenticated_client, car):
    url = reverse('car-update', args=[car.id])
    data = {
        "seating_capacity": 7
    }
    response = authenticated_client.put(url, data)
    assert response.status_code == 200
    assert response.data["message"] == "Car updated successfully"
    assert response.data["data"]["seating_capacity"] == 7
@pytest.mark.django_db
def test_delete_car(authenticated_client, car):
    url = reverse('car-delete', args=[car.id])
    response = authenticated_client.delete(url)
    assert response.status_code == 200
    assert response.data["message"] == "Car deleted successfully"
    assert not Car.objects.filter(id=car.id).exists()
