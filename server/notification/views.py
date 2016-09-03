from rest_framework import views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import NotificationSerializer
from .models import Notification


class NotificationView(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)


class NotificationReadView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pk = request.GET.get('id', 0)
        user = request.user
        notification = Notification.objects.get(pk=pk)
        if notification.user != user:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        notification.is_read = True
        notification.save()

        return Response({'result': 'success'})
