from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication


class WSTokenAuthentication(TokenAuthentication):

    def __init__(self, request):
        self.process_request(request)

    def process_request(self, request):
        try:
            auth = request.GET.get('token', None).split()
        except:
            raise PermissionDenied()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise PermissionDenied(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise PermissionDenied(msg)

        user = self.authenticate_credentials(auth[1])[0]
        # request.user = SimpleLazyObject(user)
        request.user = user
