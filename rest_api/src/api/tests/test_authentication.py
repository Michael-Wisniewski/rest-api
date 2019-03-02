from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
import pytest
import json
import jwt

@pytest.mark.django_db
class TestJWTAuthentication(TestCase):

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_jwt_refresh(self):
        get_keys_path = reverse('api:token_obtain_pair')
        refresh_keys_path = reverse('api:token_refresh')
        client = Client()
        User.objects.create_user(username='admin', password='admin')
        user_auth_data = {'username': 'admin', 'password': 'admin'}
        response = client.post(get_keys_path, user_auth_data, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        response = client.post(refresh_keys_path, { 'refresh': response_data['refresh']}, format='json')
        self.assertEqual(response.status_code, 200)