from django.contrib.gis import admin
from .models import PointModel, LineModel
# Register your models here.

admin.site.register(PointModel, admin.GeoModelAdmin)
admin.site.register(LineModel, admin.ModelAdmin)
