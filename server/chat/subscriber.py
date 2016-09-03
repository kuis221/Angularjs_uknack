import json

from django.contrib.auth import get_user_model
from ws4redis.subscriber import RedisSubscriber
from ws4redis.redis_store import RedisMessage

from .models import Message

User = get_user_model()


class ChatSubscriber(RedisSubscriber):
    def publish_message(self, message, expire=None):
        msg = json.loads(message.decode('utf-8'))
        try:
            m = Message.objects.create(sender=User.objects.get(pk=int(msg['sender_data']['id'])),
                                       receipt=User.objects.get(pk=int(msg['receipt_data']['id'])),
                                       body=msg['message'])
            msg['created_at'] = m.created_at.strftime(Message.CREATED_AT_FORMAT)
        except:
            pass

        message = RedisMessage(json.dumps(msg).encode('utf-8'))
        super(ChatSubscriber, self).publish_message(message, expire)
