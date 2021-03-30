from django.test import TestCase
from .models import Stuff
# Create your tests here.
class StuffStrTest(TestCase):
    def test_matchName(self):
        name = "Thomas"
        n = Stuff(name = name)
        self.assertEqual(name,str(n))