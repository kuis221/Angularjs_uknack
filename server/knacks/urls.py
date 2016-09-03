from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'knacks', views.KnackViewSet)
router.register(r'knack_ideas', views.KnackIdeaViewSet)
# router.register(r'miles', views.miles_list_view)
# router.register(r'how_charge', views.charge_list_view)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^miles', 'knacks.views.miles_list_view'),
    url(r'^how_charge', 'knacks.views.charge_list_view'),
    url(r'^types', 'knacks.views.types_list_view')
]
