from django.contrib.gis.db import models

# Create your models here.


class PointModel(models.Model):
    geom = models.PointField()
    score = models.IntegerField()

    def __str__(self):
        return "%d: (%f, %f) Sc: %d" % (self.id, self.geom.coords[0], self.geom.coords[1], self.score)


class LineModel(models.Model):
    from_point = models.ForeignKey(to='PointModel', on_delete=models.PROTECT, related_name='from_point')
    to_point = models.ForeignKey(to='PointModel', on_delete=models.PROTECT, related_name='to_point')

    def __str__(self):
        return str(self.from_point.id) + " -> " + str(self.to_point.id)
