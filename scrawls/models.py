from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

def expiration_date():
    return timezone.now() + timezone.timedelta(days=2)

class Wall(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    point = models.PointField(blank = True, null=True, srid=4326)

    def save(self, *args, **kwargs):
        self.point = Point(self.lng, self.lat)
        super(Wall, self).save(*args, **kwargs)

    def order_by_dist(point):
        return Wall.objects.annotate(distance=Distance('point', point))

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
