from django.db import models
from django.utils import timezone
# Create your models here.

def expiration_date():
    return timezone.now() + timezone.timedelta(days=2)

class Wall(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()
    range = models.FloatField()

    @property
    def comments(self):
        return self.comment_set.all()

    def __str__(self):
        return self.name

class Comment(models.Model):
    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=expiration_date)

    def __str__(self):
        return self.comment
