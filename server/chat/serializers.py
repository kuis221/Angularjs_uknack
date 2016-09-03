from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Q

from .models import Message
from user_auth.serializers import PublicProfileSerializer


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = PublicProfileSerializer()
    receipt = PublicProfileSerializer()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = []

    def get_created_at(self, obj):
        return obj.created_at.strftime(Message.CREATED_AT_FORMAT)


class MessageContactSerializer(PublicProfileSerializer):
    last_message = serializers.SerializerMethodField('get_last_msg')
    last_received_at = serializers.SerializerMethodField('get_last_msg_received_at')
    owner_id = serializers.IntegerField(source='id')

    class Meta:
        model = User
        fields = ('email', 'full_name', 'age', 'college', 'picture', 'owner_id', 'username',
                  'social_links', 'descriptions', 'id', 'last_message', 'last_received_at', 'is_online')

    def get_last_msg(self, obj):
        last_message = Message.objects.filter(Q(receipt=obj.id) | Q(sender=obj.id)).first().body
        if not last_message:
            last_message = ''
        return last_message

    def get_last_msg_received_at(self, obj):
        last_received = Message.objects.filter(Q(receipt=obj.id) | Q(sender=obj.id)).first().created_at
        if last_received:
            return last_received.strftime(Message.CREATED_AT_FORMAT)
        else:
            return ''
