from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from post.models import Post
import json


class PostCreateAPITest(APITestCase):
    login_url = reverse("token_obtain_pair")
    url_create = reverse("post:create")
    url_list = reverse("post:list")

    def setUp(self):
        self.username = "oguzhan1234"
        self.password = "sifre1234"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.login_url, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_add_new_post(self):
        data = {
            "content": "icerik",
            "title": "baslik"
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)

    def test_add_new_post_unauth(self):
        self.client.credentials()
        data = {
            "content": "icerik",
            "title": "baslik"
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(401, response.status_code)

    def test_post(self):
        self.test_add_new_post()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)["results"]) == Post.objects.all().count())

class PostUpdateDelete(APITestCase):

    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yakocan"
        self.password = "deneme358"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="yakocan40.2", password=self.password)
        self.test_jwt_auth()
        self.post = Post.objects.create(title="başlık", content="içerik")
        self.url = reverse("post:update", kwargs={"slug":self.post.slug})

    def test_jwt_auth(self,username="yakocan",password="deneme358"):
        response = self.client.post(self.url_login, {"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_post_del(self):
        response=self.client.delete(self.url)
        self.assertEqual(204,response.status_code)
    def test_post_del_others(self):
        self.test_jwt_auth("yakocan40.2")
        response=self.client.delete(self.url)
        self.assertEqual(403,response.status_code)
    def test_post_update(self):
        data={
            "content":"asdasd",
            "title":"zxczxcz"
        }
        response=self.client.put(self.url,data)
        self.assertEqual(200,response.status_code)
        self.assertTrue(Post.objects.get(id=self.post.id).content==data["content"])
        
    def test_post_update_others(self):
        self.test_jwt_auth("yakocan40.2")
        data={
            "content":"asdasd",
            "title":"zxczxcz"
        }
        response=self.client.put(self.url,data)
        self.assertEqual(403,response.status_code)
        self.assertFalse(Post.objects.get(id=self.post.id).content==data["content"])

    def test_unauth(self):
        self.client.credentials()
        response=self.client.get(self.url)
        self.assertEqual(401,response.status_code)