from django.conf.urls import url
from .views import NotificationView, NotificationReadView

urlpatterns = [
    url(r'^profile/notifications$',  NotificationView.as_view({'get': 'list'})),
    url(r'^profile/notifications/read$', NotificationReadView.as_view()),
]
