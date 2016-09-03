from django.core.exceptions import ObjectDoesNotExist

from .models import KnackUser
from .serializers import AuthTokenSerializer


def associate_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = KnackUser.objects.get(email=email)
    except:
        pass
    return kwargs


# User details pipeline
def user_details(strategy, details, response, user=None, *args, **kwargs):

    serializer_class = AuthTokenSerializer
    """Update user details using data from provider."""
    if user:
        email, password = '', ''
        password = response['access_token']
        email = response['email']
        data = {'email': email, 'password': password}
        if kwargs['backend'].name == 'facebook':
            try:
                KnackUser.objects.get(email=data['email'])
            except ObjectDoesNotExist:
                KnackUser.objects.create_user(data['email'], data['password'])

            serializer = serializer_class(data=data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
