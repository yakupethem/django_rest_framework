from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.utils import json


class UserRegistrationTestCase(APITestCase):
    url=reverse("account:register")
    url_login=reverse("token_obtain_pair")

    def test_user_registration(self):
        data={
            "username":"yakocan40test",
            "password":"deneme123"
        }
        response = self.client.post(self.url,data)
        self.assertEqual(201,response.status_code)

    def test_user_invalid_password(self):
        data = {
            "username": "yakocan40test",
            "password": "1"
        }
        response = self.client.post(self.url,data)
        self.assertEqual(400,response.status_code)

    def test_unique_name(self):

        self.test_user_registration()
        data = {
            "username": "yakocan40test",
            "password": "asdasdasd213123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        self.test_user_registration()
        self.client.login(username="yakocan40test",password="deneme123")
        response=self.client.get(self.url)
        self.assertEqual(403,response.status_code)

    def test_user_token_auth_regis(self):
        self.test_user_registration()
        data = {
            "username": "yakocan40test",
            "password": "deneme123"
        }
        response=self.client.post(self.url_login,data)
        self.assertEqual(200,response.status_code)
        token=response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

        response2=self.client.get(self.url)
        self.assertEqual(403,response2.status_code)

class UserLogin(APITestCase):
    url_login=reverse("token_obtain_pair")

    def setUp(self):
        self.username="yakocan"
        self.password="deneme358"
        self.user=User.objects.create_user(username=self.username,password=self.password)

    def test_user_token(self):
        response=self.client.post(self.url_login,{"username":"yakocan","password":"deneme358"})
        self.assertEqual(200,response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        response=self.client.post(self.url_login,{"username":"qweqasdaszxz","password":"deneme358"})
        self.assertEqual(401,response.status_code)

    def empty(self):
        response=self.client.post(self.url_login,{"username":"","password":""})
        self.assertEqual(400,response.status_code)

class UserPasswordChange(APITestCase):
    url_login = reverse("token_obtain_pair")
    url = reverse("account:changepassword")
    def setUp(self):
        self.username="yakocan"
        self.password="deneme358"
        self.user=User.objects.create_user(username=self.username,password=self.password)
    def login_with_token(self):
        data = {
            "username": "yakocan",
            "password": "deneme358"
        }

        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    def test_is_auth_user(self):
        response=self.client.get(self.url)
        self.assertEqual(401,response.status_code)

    def test_valid_info(self):
        self.login_with_token()
        data = {
            "old_password": "deneme358",
            "new_password": "deneme1358"
        }
        response=self.client.put(self.url,data)
        self.assertEqual(204,response.status_code)
    def test_wrong_info(self):
        self.login_with_token()
        data = {
            "old_password": "zxcdsa",
            "new_password": "zvcsdss"
        }
        response=self.client.put(self.url,data)
        self.assertEqual(400,response.status_code)
    def test_empty_info(self):
        self.login_with_token()
        data = {
            "old_password": "",
            "new_password": ""
        }
        response=self.client.put(self.url,data)
        self.assertEqual(400,response.status_code)


class UserProfilUpdate(APITestCase):
    url_login = reverse("token_obtain_pair")
    url = reverse("account:me")

    def setUp(self):
        self.username = "yakocan"
        self.password = "deneme358"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username": "yakocan",
            "password": "deneme358"
        }

        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    def test_is_auth_user(self):
        response=self.client.get(self.url)
        self.assertEqual(401,response.status_code)
    def test_valid_info(self):
        self.login_with_token()
        data = {

                "id": 1,
                "first_name": "",
                "last_name": "",
                "profile": {
                    "id": 1,
                    "note": "",
                    "twitter": "asd"
    }
}

        response=self.client.put(self.url,data,format="json")
        self.assertEqual(200,response.status_code)
        self.assertEqual(json.loads(response.content),data)

    def test_empty_info(self):
        self.login_with_token()
        data = {

                    "id": 1,
                    "first_name": "",
                    "last_name": "",
                    "profile": {
                        "id": 1,
                        "note": "",
                        "twitter": ""
                        }

        }
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(200, response.status_code)