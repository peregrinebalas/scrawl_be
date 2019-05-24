import datetime
import json

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Wall, Comment
from .serializers import WallsSerializer


client = APIClient()
class PostWallTests(APITestCase):

    def test_a_wall_can_be_added(self):
        url = reverse('scrawls:walls-create')
        data = json.dumps(
            {
                'name': 'The Basement',
                'lat': 25.3454567,
                'lng': 90.1234567,
                'comment': 'Learn to code!'
            }
        )

        response = client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'name': 'The Basement',
            'lat': 25.3454567,
            'lng': 90.1234567,
            'comments': ['Learn to code!']
        })

    def test_a_wall_requires_all_fields_to_be_added(self):
        url = reverse('scrawls:walls-create')
        data1 = json.dumps(
            {
                'name': 'The Basement',
                'lng': 90.1234567,
            }
        )
        data2 = json.dumps(
            {
                'name': 'The Basement',
                'lat': 25.3454567,
            }
        )
        data3 = json.dumps(
            {
                'lat': 25.3454567,
                'lng': 90.1234567,
            }
        )

        response1 = client.post(url, data=data1, content_type='application/json')
        self.assertEqual(response1.status_code, 409)
        self.assertEqual(response1.data, {'error': 'Fields missing, could not save wall.'})
        response2 = client.post(url, data=data2, content_type='application/json')
        self.assertEqual(response2.status_code, 409)
        self.assertEqual(response2.data, {'error': 'Fields missing, could not save wall.'})
        response3 = client.post(url, data=data3, content_type='application/json')
        self.assertEqual(response3.status_code, 409)
        self.assertEqual(response3.data, {'error': 'Fields missing, could not save wall.'})

class WallShowTests(APITestCase):

    def setUp(self):
        self.turing = Wall.objects.create(
            name='Turing School of Software & Design', lat=25.3454567, lng=90.1234567)

        self.comment_1 = Comment.objects.create(
            wall= self.turing, comment='Turing School is a place')

    def test_it_can_get_a_specific_wall(self):
        url = reverse('scrawls:wall-show', kwargs={'pk': self.turing.pk})
        wall = Wall.objects.get(pk=self.turing.pk)
        serializer = WallsSerializer(wall)
        response = client.get(url, serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_it_cannot_get_a_specific_wall(self):
        response = client.get(reverse('scrawls:wall-show', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], "Could Not Find Wall")

class CreateCommentTests(APITestCase):
    def setUp(self):
        self.turing = Wall.objects.create(
            name='Turing School of Software & Design', lat=25.3454567, lng=90.1234567)

        self.comment_1 = Comment.objects.create(
            wall= self.turing, comment='Turing School is a place')

        self.body = {"comment": "There's a Fish Monster"}

    def test_it_post_to_a_specific_wall(self):
        url = reverse('scrawls:comments-create', kwargs={"pk": self.turing.pk})
        response = client.post(url, self.body, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.message, "Comment Saved!")

    def test_it_cannot_post_to_a_specific_wall(test_a_wall_requires_all_fields_to_be_added):
        url = reverse('scrawls:comments-create', kwargs={"pk": 100})
        response = client.post(url, body, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.message, "Could Not Find Wall")




class ModelTests(TestCase):

    def test_it_exists(self):
        wall = Wall.objects.create(name='Wall', lat=3.5, lng=3.5)
        all = Wall.objects.all()
        self.assertIs(all.count(), 1)
