import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Wall, Comment

class WallModelTests(TestCase):

    def test_it_exists(self):
        wall = Wall.objects.create(name='Wall', address='100 St.', lat=3.5, lng=3.5, range=3.5)
        all = Wall.objects.all()
        self.assertIs(all.count(), 1)
