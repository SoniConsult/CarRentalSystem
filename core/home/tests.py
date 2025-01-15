import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from home.models import Car


@pytest.mark.django_db
class TestAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_register(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Registration successfully"

    def test_login(self):
        # First, create a user to log in
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        url = reverse('login')
        data = {
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_add_car(self):
        # Login the user
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        url = reverse('addCar')
        data = {
            "make": "Toyota",
            "model": "Camry",
            "year": 2021
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "Car added successfully"

    def test_get_car_detail(self):
        # Login the user
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Add a car
        car = Car.objects.create(make="Toyota", model="Camry", year=2021, owner=user)

        url = reverse('car_detail', args=[car.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["make"] == "Toyota"

    def test_update_car(self):
        # Login the user
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Add a car
        car = Car.objects.create(make="Toyota", model="Camry", year=2021, owner=user)

        url = reverse('car_update', args=[car.id])
        data = {
            "model": "Corolla",
            "year": 2022
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Car updated successfully"
        assert response.data["data"]["model"] == "Corolla"

    def test_delete_car(self):
        # Login the user
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Add a car
        car = Car.objects.create(make="Toyota", model="Camry", year=2021, owner=user)

        url = reverse('car_delete', args=[car.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Car deleted successfully"
        assert Car.objects.count() == 0  # Check that the car was deleted
