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
            "password": "testpassword",
            "role":"Admin"
        }
        response = self.client.post(url, data, format='json')
        print(response.status_code)  # Print the status code
        print(response.data)   
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Registration successfully"

   
    def test_login(self):
        # First, create a user to log in
        user = User.objects.create_user(username="abc",email="abc@example.com", password="abc")
        url = reverse('login')
        data = {
            "email": "abc@example.com",
            "password": "abc"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data