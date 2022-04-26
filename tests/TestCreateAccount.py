from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

import StuffTracker.models
from StuffTracker.models import MyUser, Stuff


class TestCreateSuccess(TestCase):
    client = None

    def setUp(self):
        self.client = Client()

    def test_newUserAnyPassRedirect(self):
        response = self.client.post("/", {"name": "newuser", "password": "newuser"}, follow=True)
        self.assertRedirects(response, "/things/", msg_prefix="Invalid redirect for account creation success")

    def test_newUserAnyPassDatabase(self):
        response = self.client.post("/", {"name": "newuser", "password": "newuser"}, follow=True)
        user = MyUser.objects.get(name="newuser")
        self.assertEquals("newuser", user.name, msg="User Creation failed: invalid name after database query.")
        self.assertEquals("newuser", user.password, msg="User Creation failed: invalid password after database query.")


class TestCreateMissingPassword(TestCase):
    client = None

    def setUp(self):
        self.client = Client()

    def test_newUserEmptyPassRedirect(self):
        response = self.client.post("/", {"name": "newuser", "password": ""}, follow=True)
        self.assertRedirects(response, "/", msg_prefix="Invalid redirect for account creation failure: empty password")

    def test_newUserEmptyPassDatabase(self):
        response = self.client.post("/", {"name": "newuser", "password": ""}, follow=True)
        with self.assertRaises(ObjectDoesNotExist, msg="User creation failed: did not error on empty password."):
            user = MyUser.objects.get(name="newuser")

    def test_newUserEmptyPassMessage(self):
        response = self.client.post("/", {"name": "newuser", "password": ""}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid password.",
                         msg="Missing error message on empty password.")


class TestCreateMissingUsername(TestCase):
    client = None

    def setUp(self):
        self.client = Client()

    def test_emptyUserYesPassRedirect(self):
        response = self.client.post("/", {"name": "", "password": "test"}, follow=True)
        self.assertRedirects(response, "/",
                             msg_prefix="Invalid redirect for account creation failure: empty username, valid password")

    def test_emptyUserYesPassDatabase(self):
        response = self.client.post("/", {"name": "", "password": "test"}, follow=True)
        with self.assertRaises(ObjectDoesNotExist, msg="User creation failed: did not error on empty username."):
            user = MyUser.objects.get(name="")

    def test_emptyUserYesPassMessage(self):
        response = self.client.post("/", {"name": "", "password": "test"}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid username.",
                         msg="Missing error message on empty username and empty password.")

    def test_emptyUserEmptyPassRedirect(self):
        response = self.client.post("/", {"name": "", "password": ""}, follow=True)
        self.assertRedirects(response, "/",
                             msg_prefix="Invalid redirect for account creation failure: empty username, empty pass")

    def test_emptyUserEmptyPassDatabase(self):
        response = self.client.post("/", {"name": "", "password": ""}, follow=True)
        with self.assertRaises(ObjectDoesNotExist,
                               msg="User creation failed: did not error on empty username and password."):
            user = MyUser.objects.get(name="")

    def test_emptyUserEmptyPassMessage(self):
        response = self.client.post("/", {"name": "", "password": ""}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid username.",
                         msg="Missing error message on empty username and empty password.")


class TestCreateSpaces(TestCase):
    client = None

    def setUp(self):
        self.client = Client()

    def test_spacesLeadingRedirect(self):
        response = self.client.post("/", {"name": "   test", "password": "test"}, follow=True)
        self.assertRedirects(response, "/", msg_prefix="Invalid redirect for account creation failure: leading spaces")

    def test_spacesLeadingDatabase(self):
        response = self.client.post("/", {"name": "   test", "password": "test"}, follow=True)
        with self.assertRaises(ObjectDoesNotExist, msg="Did not error on leading spaces in username."):
            user = MyUser.objects.get(name="   test")

    def test_spacesLeadingMessage(self):
        response = self.client.post("/", {"name": "   test", "password": "test"}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid username.",
                         msg="Missing error message on leading spaces in username.")

    def test_spacesTrailingRedirect(self):
        response = self.client.post("/", {"name": "test   ", "password": "test"}, follow=True)
        self.assertRedirects(response, "/", msg_prefix="Invalid redirect for account creation failure: trailing spaces")

    def test_spacesTrailingDatabase(self):
        response = self.client.post("/", {"name": "test   ", "password": "test"}, follow=True)
        with self.assertRaises(ObjectDoesNotExist, msg="Did not error on trailing spaces in username."):
            user = MyUser.objects.get(name="test   ")

    def test_spacesTrailingMessage(self):
        response = self.client.post("/", {"name": "test   ", "password": "test"}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid username.",
                         msg="Missing error message on trailing spaces in username.")

    def test_spacesBothEndsRedirect(self):
        response = self.client.post("/", {"name": "   test   ", "password": "test"}, follow=True)
        self.assertRedirects(response, "/", msg_prefix="Invalid redirect for account creation failure: both-end spaces")

    def test_spacesBothEndsDatabase(self):
        response = self.client.post("/", {"name": "   test   ", "password": "test"}, follow=True)
        with self.assertRaises(ObjectDoesNotExist, msg="Did not error on  both-end spaces in username."):
            user = MyUser.objects.get(name="   test   ")

    def test_spacesBothEndsMessage(self):
        response = self.client.post("/", {"name": "   test   ", "password": "test"}, follow=True)
        self.assertTrue("message" in response.context, msg="Message not present in context: bad redirect?.")
        self.assertEqual(response.context["message"], "Error: invalid username.",
                         msg="Missing error message on both-end spaces in username.")
