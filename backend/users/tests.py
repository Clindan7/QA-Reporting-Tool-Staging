import unittest
from unittest.mock import patch

import requests
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from requests import Response

from rest_framework import status
from rest_framework.test import APIClient
from users.serializer import MemberSerializer

from core import custom_errors
from users import user_errors
from users.models.members import Members
from users.views import (
    generate_refresh_token,
    google_login,
    fetch_user_by_email, extract_user_info,
)


class GoogleLoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    @patch('users.views.extract_user_info')
    def test_google_login_failure(self, mock_extract_user_info):
        mock_extract_user_info.return_value = None  # Simulating inability to extract user info

        request_data = {"access_token": "mocked_access_token"}
        request = self.factory.post('/google-login/', request_data)

        response = google_login(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, user_errors.TOKEN_ERROR)  # Check the expected error message


    def test_google_login_failed(self):
        # Create a request with the required data
        request = self.factory.post(
            '/google-login/', {'access_token': 'mocked_access_token'})
        # Call the view function
        response = google_login(request)
        self.assertEqual(response.status_code, 400)


class AccessTokenGenerationTestCase(TestCase):
    def setUp(self):
        # Create a test user and obtain a refresh token
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@example.com')
        self.refresh_token = generate_refresh_token(self.user.email)
        self.api_client = APIClient()

    def test_access_token_generation_success(self):
        # Assuming you have a name for your view
        url = reverse('create_access_token_from_refresh_token')
        data = {'refresh_token': self.refresh_token}
        response = self.api_client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Refresh_Token', response.data)
        self.assertIn('Access_Token', response.data)

    def test_missing_required_fields(self):
        url = reverse('create_access_token_from_refresh_token')
        data = {}  # Missing 'refresh_token'

        response = self.api_client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, custom_errors.MISSING_REQUIRED_FIELDS)

    def test_expired_refresh_token(self):
        # Simulate an expired refresh token
        expired_refresh_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imthbm5hbi5wQGlubm92YXR1cmVsYWJzLmNvbSIsInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNjk3MDE0NTYyfQ.pLei04ugMAqrGDqssEhxKdQ3BxykexjGZralTinbPEk"

        url = reverse('create_access_token_from_refresh_token')
        data = {'refresh_token': expired_refresh_token}

        response = self.api_client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_internal_server_error(self):
        # Simulate an internal server error in the view
        url = reverse('create_access_token_from_refresh_token')
        data = {'refresh_token': self.refresh_token}

        # Mock the generate_access_token function to raise an exception
        with unittest.mock.patch('users.views.generate_access_token') as mock_generate_access_token:
            mock_generate_access_token.side_effect = Exception("Simulated internal server error")

            response = self.api_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_fetch_user_by_email_exists(self):
        user_email = "user@example.com"
        user_name = 'John Doe'
        # Create a test user
        test_user = Members.objects.create(email=user_email, name=user_name,role_type=1,status=1)

        # Call the fetch_user_by_email function
        result = fetch_user_by_email(user_email)

        # Assert that the function returns the correct user
        self.assertEqual(result, test_user)

    def test_fetch_user_by_email_not_exists(self):
        # Call the fetch_user_by_email function for a non-existing user
        result = fetch_user_by_email('nonexistent@example.com')

        # Assert that the function returns None for non-existing user
        
        self.assertIsNone(result)

class GetAllUsersAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some sample users for testing
        Members.objects.create(name="User1", email="user1@example.com",role_type=2, user_id=1, status="1")
        Members.objects.create(name="User2", email="user2@example.com",role_type=2, user_id=2, status="0")

    def test_get_all_users(self):
        # Ensure the API view returns a 200 status code and the correct data
        response = self.client.get('/users/userlist')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Serialize the sample data to compare with the response data
        users = Members.objects.all()
        serializer = MemberSerializer(users, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    
  
class GetUserByIdAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Members.objects.create(name="User1", email="user1@example.com",role_type=2, user_id=1, status="1")
        Members.objects.create(name="User2", email="user2@example.com",role_type=2, user_id=2, status="0")

    def test_get_user_by_id(self):
        url = reverse('get_user_by_id')  # Use the actual URL name you have defined in your Django urls.py
        user_id = 1  # Use a valid user ID that you have created in your setup
        response = self.client.get(url, {'userid': user_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id_invalid_user(self):
       url = reverse('get_user_by_id')  # Use the actual URL name you have defined in your Django urls.py
     
       response = self.client.get(url, {'userid': "ttttt"}, format='json')

       self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch('users.views.verify_google_access_token')
    @patch('users.views.requests.get')
    def test_extract_user_info(self, mock_requests_get, mock_verify_google_access_token):
        mock_verify_google_access_token.return_value = True
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b'{"email": "example@gmail.com", "name": "sample"}'
        mock_requests_get.return_value = mock_response
        response = extract_user_info("sample_token")
        self.assertEqual(response, ("example@gmail.com", "sample"))


    @patch('users.views.verify_google_access_token')
    @patch('users.views.requests.get')
    def test_extract_user_info_error(self, mock_requests_get, mock_verify_google_access_token):
        mock_verify_google_access_token.return_value = True
        mock_response = Response()
        mock_response.status_code = 400
        mock_response._content = None
        mock_requests_get.return_value = mock_response
        response = extract_user_info("sample_token")
        self.assertEqual(response, None)

    @patch('users.views.verify_google_access_token')
    @patch('users.views.requests.get')
    def test_extract_user_info_exception(self, mock_requests_get, mock_verify_google_access_token):
        mock_verify_google_access_token.return_value = True
        mock_requests_get.side_effect = requests.RequestException("e")
        response = extract_user_info("sample_token")
        self.assertEqual(response.status_code, 500)