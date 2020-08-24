from rest_framework import routers
from .views import PointViewSet

router = routers.SimpleRouter()
router.register('point', PointViewSet)

urlpatterns = router.urls
