import datetime
import json

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Wall, Comment

client = APIClient()
class PostWallTests(APITestCase):

    def test_a_wall_can_be_added(self):
        url = reverse('scrawls:walls-create')
        data = json.dumps(
            {
                'name': 'Turing School of Software & Design',
                'address': '1331 17th Street, Denver, CO, USA',
                'lat': 25.3454567,
                'lng': 90.1234567,
                'range': 0.0101234
            }
        )

        response = client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'message': 'Turing School of Software & Design can be found at 1331 17th Street, Denver, CO, USA.'})

# class WallShowTests(APITestCase):
#
#     def test_it_can_get_a_specific_wall(self, **kwargs):
#         url = reverse('scrawls:wall-show')
#         data = json.dumps(
#             {
#                 'name': 'Turing School of Software & Design',
#                 'address': '1331 17th Street, Denver, CO, USA',
#                 'lat': 25.3454567,
#                 'lng': 90.1234567,
#                 'range': 0.0101234,
#                 'comments': {
#                     "comment": "I'm a comment"
#                     }
#             }
#         )
#
#         response = client.get(url, data=data, content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data, {'message': 'Turing School of Software & Design can be found at 1331 17th Street, Denver, CO, USA.'})

class ModelTests(TestCase):

    def test_it_exists(self):
        wall = Wall.objects.create(name='Wall', address='100 St.', lat=3.5, lng=3.5, range=3.5)
        all = Wall.objects.all()
        self.assertIs(all.count(), 1)
