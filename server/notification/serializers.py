from rest_framework import serializers
from django.contrib.auth import get_user_model

from user_auth.serializers import BasicProfileSerializer
from .models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    sender = BasicProfileSerializer()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'sender', 'data', 'type', 'is_read', 'created_at')

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d/%y')
