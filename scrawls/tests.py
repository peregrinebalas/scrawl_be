import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Wall, Comment


def create_wall(loc_data):
    
