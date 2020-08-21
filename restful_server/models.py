from django.contrib.gis.db import models

# Create your models here.


class PointModel(models.Model):
    geom = models.PointField()
    score = models.IntegerField()


class LineModel(models.Model):
    from_point = models.ForeignKey(to='PointModel', on_delete=models.PROTECT, related_name='from_point')
    to_point = models.ForeignKey(to='PointModel', on_delete=models.PROTECT, related_name='to_point')
