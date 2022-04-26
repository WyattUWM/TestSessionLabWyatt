from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

import StuffTracker.models
from StuffTracker.models import MyUser, Stuff


class TestLoginSuccess(TestCase):
    client = None
    users = None

    def setUp(self):
        self.client = Client()
        self.users = {"wyatt": ["wyatt1", "wyatt2"], "admin": ["admin1", "admin2"], "test": ["test1", "test2"]}

        # Save each user with same user and pass
        for i in self.users.keys():
            temp = MyUser(name=i, password=i)
            temp.save()

            # Save each user's stuff
            for j in self.users[i]:
                Stuff(name=j, owner=temp).save()

    def test_ExistUserRightPassRedirect(self):
        response = self.client.post("/", {"name": "wyatt", "password": "wyatt"}, follow=True)
        self.assertRedirects(response, "/things/", msg_prefix="Invalid redirect for existent user right pass login")

    def test_ExistUserRightPassItemList(self):
        response = self.client.post("/", {"name": "wyatt", "password": "wyatt"}, follow=True)

        user = MyUser.objects.get(name="wyatt")
        Stuff.objects.get(name="wyatt1", owner=user)

    def test_ExistUserRightPassInvalidItem(self):
        response = self.client.post("/", {"name": "wyatt", "password": "wyatt"}, follow=True)

        user = MyUser.objects.get(name="wyatt")
        with self.assertRaises(ObjectDoesNotExist):
            Stuff.objects.get(name="admin1", owner=user)


class TestLoginWrongPass(TestCase):
    client = None
    users = None

    def setUp(self):
        self.client = Client()
        self.users = {"wyatt": ["wyatt1", "wyatt2"]}

        # Save each user with same user and pass
        for i in self.users.keys():
            temp = MyUser(name=i, password=i)
            temp.save()

            # Save each user's stuff
            for j in self.users[i]:
                Stuff(name=j, owner=temp).save()

    def test_ExistUserWrongPassRedirect(self):
        response = self.client.post("/", {"name": "wyatt", "password": "wrong"}, follow=True)
        self.assertRedirects(response, "/", msg_prefix="Invalid redirect for existent user wrong pass login")

    def test_ExistUserWrongPassMessage(self):
        response = self.client.post("/", {"name": "wyatt", "password": "wrong"}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context on invalid password: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid password.",
                         msg="Missing error message on invalid password.")


class TestLoginNoPass(TestCase):
    client = None
    users = None

    def setUp(self):
        self.client = Client()
        self.users = {"wyatt": ["wyatt1", "wyatt2"]}

        # Save each user with same user and pass
        for i in self.users.keys():
            temp = MyUser(name=i, password=i)
            temp.save()

            # Save each user's stuff
            for j in self.users[i]:
                Stuff(name=j, owner=temp).save()

    def test_ExistUserEmptyPassRedirect(self):
        response = self.client.post("/", {"name": "wyatt", "password": ""}, follow=True)
        self.assertRedirects(response, "/", msg_prefix="Invalid redirect for existent user empty pass login")

    def test_ExistUserEmptyPassMessage(self):
        response = self.client.post("/", {"name": "wyatt", "password": ""}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context on empty password: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid password.",
                         msg="Missing error message on empty password.")
