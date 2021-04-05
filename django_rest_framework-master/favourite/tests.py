from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.utils import json

from favourite.models import Favourite
from post.models import Post


class FavouriteCreateList(APITestCase):
    url = reverse("favourite:list-create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yakocan"
        self.password = "deneme358"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_auth()
        self.post = Post.objects.create(title="başlık", content="içerik")

    def test_jwt_auth(self):
        response = self.client.post(self.url_login, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_add_fav(self):
        data = {
            "content": "içerik güzel",
            "user": self.user.id,
            "post": self.post.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_favs(self):
        self.test_add_fav()
        response = self.client.get(self.url)
        self.assertTrue(
            len(json.loads(response.content)["results"])
            == Favourite.objects.filter(user=self.user).count())

class FavouriteUpdateDelete(APITestCase):

    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yakocan"
        self.password = "deneme358"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="yakocan40.2", password=self.password)
        self.test_jwt_auth()
        self.post = Post.objects.create(title="başlık", content="içerik")
        self.favourite=Favourite.objects.create(content="deneme",post=self.post,user=self.user)
        self.url = reverse("favourite:update-delete", kwargs={"pk":self.favourite.pk})

    def test_jwt_auth(self,username="yakocan",password="deneme358"):
        response = self.client.post(self.url_login, {"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_fav_del(self):
        response=self.client.delete(self.url)
        self.assertEqual(204,response.status_code)

    def test_fav_del_anotherUser(self):
        self.test_jwt_auth("yakocan40.2")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_fav_update(self):
        data={"content":"içerik321"}
        response=self.client.put(self.url,data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Favourite.objects.get(id=self.favourite.id).content==data["content"])

    def test_fav_update_anotherUser(self):
        self.test_jwt_auth("yakocan40.2")
        data={
            "content":"içerik2",
            "user":self.user.id
        }
        response=self.client.put(self.url,data)
        self.assertTrue(403,response.status_code)

    def test_nouser(self):
        self.client.credentials()
        response=self.client.get(self.url)
        self.assertEqual(401,response.status_code)

