from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
