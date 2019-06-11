import datetime
import json

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status

from .models import Wall, Comment
from .serializers import WallSerializer, WallsSerializer


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
                'lng': 90.1234567
            }
        )
        data2 = json.dumps(
            {
                'name': 'The Basement',
                'lat': 25.3454567
            }
        )
        data3 = json.dumps(
            {
                'lat': 25.3454567,
                'lng': 90.1234567
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

    def test_a_wall_cant_be_added_too_close_to_another_wall(self):
        wall = Wall.objects.create(
            name = 'The Basement',
            lat = 25.3454567,
            lng = 90.1234567
        )
        wall.comment_set.create(comment = 'Learn to code!')
        data = json.dumps({
            'name': 'Stacks on Stacks',
            'lat': 25.3454567 + 0.0014,
            'lng': 90.1234567 + 0.0015,
            'comment': 'the sub hub'
        })
        url = reverse('scrawls:walls-create')

        response = client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data, {
            "error": "Too close to another wall to create at your current location."
        })

class WallShowTests(APITestCase):

    def setUp(self):
        self.turing = Wall.objects.create(
            name='Turing School of Software & Design', lat=25.3454567, lng=90.1234567)

        self.comment1 = Comment.objects.create(
            wall= self.turing, comment='Turing School is a place')

    def test_it_can_get_a_specific_wall(self):
        url = reverse('scrawls:wall-show', kwargs={'pk': self.turing.pk})
        wall = Wall.objects.get(pk=self.turing.pk)
        serializer = WallSerializer(wall)
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_it_cannot_get_a_specific_wall(self):
        url = reverse('scrawls:wall-show', kwargs={'pk': 100})
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], "Could Not Find Wall")

class CreateCommentTests(APITestCase):
    def setUp(self):
        self.turing = Wall.objects.create(
            name='Turing School of Software & Design', lat=25.3454567, lng=90.1234567)

        self.comment_1 = Comment.objects.create(
            wall= self.turing, comment='Turing School is a place')

        self.body = {"comment": "There's a Fish Monster"}

    def test_it_post_to_a_specific_wall(self, *args):
        self.assertEqual(self.turing.comment_set.count(), 1)
        url = reverse('scrawls:comments-create', kwargs={"pk": self.turing.pk})
        response = client.post(url, json.dumps(self.body), content_type='application/json')
        self.assertEqual(self.turing.comment_set.count(), 2)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "Comment Saved!")

    def test_it_cannot_post_to_a_specific_wall(self, *args):
        self.assertEqual(self.turing.comment_set.count(), 1)
        url = reverse('scrawls:comments-create', kwargs={"pk": 100})
        response = client.post(url, json.dumps(self.body), content_type='application/json')
        self.assertEqual(self.turing.comment_set.count(), 1)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['error'], "Conflict!")

class NearestWallsIndexTests(APITestCase):

    def setUp(self):
        #0.0015
        self.scott = Wall.objects.create(
            name="Scott's Spot", lat=25.1000001, lng=90.1000001)
        self.bsmnt = Wall.objects.create(
            name="The Basement", lat=25.0000001, lng=90.0000001)
        self.union = Wall.objects.create(
            name="Union Station", lat=25.0000001, lng=90.0030001)
        self.mca = Wall.objects.create(
            name="MCA Denver", lat=25.0030001, lng=90.0000001)
        self.amante = Wall.objects.create(
            name="Amante's", lat=25.0015001, lng=90.0000001)
        self.mrkt = Wall.objects.create(
            name="Milk Market", lat=25.0000001, lng=90.0015001)

    def test_it_returns_the_5_nearest_walls(self):
        url = reverse('scrawls:walls-nearest') + '?lat=25.0000002&lng=90.0000002'
        walls = [self.bsmnt, self.mrkt, self.amante, self.union, self.mca]
        serializer = []
        for wall in walls:
            serializer.append(WallsSerializer(wall).data)
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer)

    def test_that_without_lat_and_lng_walls_cant_be_found(self):
        url = reverse('scrawls:walls-nearest')
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'error': 'Cannot Locate Nearest Walls'})

class ModelTests(TestCase):

    def test_wall_exists(self):
        wall = Wall.objects.create(name='Wall', lat=3.5, lng=3.5)
        all = Wall.objects.all()
        self.assertIs(all.count(), 1)

    def test_comment_exists(self):
        wall = Wall.objects.create(name='Wall', lat=3.5, lng=3.5)
        comment = Comment.objects.create(wall=wall, comment='Comment')
        all = Comment.objects.all()
        self.assertIs(all.count(), 1)
