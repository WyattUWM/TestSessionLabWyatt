from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

import StuffTracker.models
from StuffTracker.models import MyUser, Stuff


class TestAddItemSuccess(TestCase):
    client = None
    users = None

    token_pass = "test"

    def setUp(self):
        self.client = Client()
        self.users = {"wyatt": ["wyatt1", "wyatt2"], "admin": ["admin1", "admin2"]}

        # Save each user with same user and pass
        for i in self.users.keys():
            temp = MyUser(name=i, password=i)
            temp.save()

    def test_addValidStringResponse(self):
        session = self.client.session
        session["name"] = "wyatt"
        session.save()

        response = self.client.post("/things/", {"stuff": self.token_pass}, follow=True)
        response_things = response.context["things"]

        self.assertIn(self.token_pass, response_things,
                      "Token not found in POST response after add: " + self.token_pass)

    def test_addValidStringDatabase(self):
        session = self.client.session
        session["name"] = "wyatt"
        session.save()

        response = self.client.post("/things/", {"stuff": self.token_pass}, follow=True)
        database_things = list(map(str, Stuff.objects.filter(owner__name="wyatt")))

        self.assertIn(self.token_pass, database_things, "Token not found in database after add: " + self.token_pass)

    def test_addValidStringOtherUser(self):
        session = self.client.session
        session["name"] = "wyatt"
        session.save()

        response = self.client.post("/things/", {"stuff": self.token_pass}, follow=True)
        database_things_admin = list(map(str, Stuff.objects.filter(owner__name="admin")))

        self.assertNotIn(self.token_pass, database_things_admin,
                         "Token found for wrong user after add: " + self.token_pass)


class TestAddItemEmpty(TestCase):
    client = None
    users = None

    token_empty = ""

    def setUp(self):
        self.client = Client()
        self.users = {"wyatt": ["wyatt1", "wyatt2"], "admin": ["admin1", "admin2"]}

        # Save each user with same user and pass
        for i in self.users.keys():
            temp = MyUser(name=i, password=i)
            temp.save()

    def test_addEmptyStringResponse(self):
        session = self.client.session
        session["name"] = "wyatt"
        session.save()

        response = self.client.post("/things/", {"stuff": self.token_empty}, follow=True)
        response_things = response.context["things"]

        self.assertNotIn(self.token_empty, response_things, "Token found in POST response after invalid empty add.")

    def test_addEmptyStringDatabase(self):
        session = self.client.session
        session["name"] = "wyatt"
        session.save()

        response = self.client.post("/things/", {"stuff": self.token_empty}, follow=True)
        database_things = list(map(str, Stuff.objects.filter(owner__name="wyatt")))

        self.assertNotIn(self.token_empty, database_things, "Token not found in database after invalid empty add.")
