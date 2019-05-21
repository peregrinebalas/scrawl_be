import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Wall, Comment

class PostWallTests(TestCase):

    def test_a_wall_can_be_added(self):
        response = self.client.post(reverse('scrawls:create'), {
            'name': 'Turing School of Software & Design',
            'address': '1331 17th Street, Denver, CO, USA',
            'lat': 25.3454567,
            'long': 90.1234567,
            'radius': 0.0101234
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, {'Turing School of Software & Design can now be found at 1331 17th Street, Denver, CO, USA'})


class ModelTests(TestCase):

    def test_it_exists(self):
        wall = Wall.objects.create(name='Wall', address='100 St.', lat=3.5, lng=3.5, range=3.5)
        all = Wall.objects.all()
        self.assertIs(all.count(), 1)
