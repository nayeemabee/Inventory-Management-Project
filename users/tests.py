import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


# Creating a logger for the tests
logger = logging.getLogger('users.tests')


class UserAuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.username = "testuser"
        self.password = "testpass123"
        
        
        logger.info("Test setup completed.")


    def test_register_success(self):
        """Test registering a new user successfully"""
        
        data = {
            "username": "newuser",
            "password": "newpass123",
        }
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User created")
        logger.info(f"User registration successful for username: {self.username}")
    
    def test_register_failure_missing_fields(self):
        """Test registration failure due to missing fields"""
        
        data = {
            "username": self.username,
        }
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        logger.error("Registration failed due to missing password")

    
    def test_login_success(self):
        """Test logging in a registered user successfully"""
        
        # Creating user for login test
        User.objects.create_user(username=self.username, password=self.password)
        
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        logger.info(f"Login successful for username: {self.username}")

    def test_login_failure_invalid_credentials(self):
        """Test login failure due to invalid credentials"""
        
        # Creating user for login test
        User.objects.create_user(username=self.username, password=self.password)
        
        data = {
            "username": self.username,
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        logger.error(f"Login failed due to invalid credentials for username: {self.username}")

    def test_login_failure_missing_fields(self):
        """Test login failure due to missing fields"""
        
        data = {
            "username": self.username,
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        logger.error("Login failed due to missing password")


