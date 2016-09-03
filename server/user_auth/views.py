import string
import random
import uuid
import datetime
import json
import re
import base64
from time import time
import six
#Django Libs
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout as django_logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.auth.hashers import make_password
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from django.conf import settings
from social.apps.django_app.default.models import Code
from social.backends.facebook import FacebookOAuth2

#Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from sorl.thumbnail import get_thumbnail

from .models import RegisterEmail, KnackUser, Year, College

#Serializers
from .serializers import (AuthTokenSerializer, CreateUserSerializer,
                          ReturnUserSerializer, ChangePasswordSerializer,
                          ForgotPasswordSerializer, ResetPasswordSerializer,
                          ProfileSerializer, RegisterEmailSerializer)

from user_auth.models import SocialLink, Description, College, Year
from notification.models import Notification



User = get_user_model()

def token_generator(size=5, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def save_to_image(instance, picture_data):
    if instance.picture and picture_data.endswith(instance.picture.url):
        return instance.picture

    if re.search(r"data:[\w/\-\.]+;\w+,.*", picture_data) is not None:
        try:
            filename = '%s_%s.png' % (instance.pk, uuid.uuid4())
            binary_data = base64.b64decode(picture_data[picture_data.index(",") + 1:])
            return ContentFile(binary_data, filename)
        except (IOError, OSError) as e:
            # TODO: log here
            print(e)
            return None
    else:
        return None


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serialized = CreateUserSerializer(data=request.data)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.data.items()}
        user = User.objects.create_user(
            **user_data
        )
        user.save()

        response = ReturnUserSerializer(instance=user).data
        response['token'] = user.auth_token.key
        response['id'] = user.id
        response['email'] = user.email
        response['fullname'] = user.full_name
        response['college'] = user.college
        response['age'] = user.age
        response['picture'] = None

        return Response(response, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_email(request):
    serialized = RegisterEmailSerializer(data=request.data)
    if serialized.is_valid():
        subject = 'Welcome to Uknack!'
        domain = Site.objects.get(pk=settings.SITE_ID).domain
        guid = uuid.uuid4().hex
        plaintext = get_template('email.txt')
        htmly = get_template('email.html')
        context = ({'uuid': guid})

        text_content = plaintext.render(context)
        html_content = htmly.render(context)

        email = serialized.validated_data['email']
        msg = EmailMultiAlternatives(subject, text_content, 'arnokuhlein@gmail.com', [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # save register email
        serialized.save(uuid=guid)
        # send_mail(subject, message, 'noreply@unacks.com', [serialized['email']])
        return Response({'email': email}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    try:
        user = request.user
        now = timezone.now()
        user.last_seen = now
        user.is_online = False
        user.save()
        user.auth_token.delete()
        django_logout(request)
        return Response({'details': 'Logged out'}, status=status.HTTP_200_OK)
    except:
        return Response({'details': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def social_login(request):
    HttpResponseRedirect("/login/facebook/")


class LoginView(APIView):

    def get(self, request, format=None):
        data = json.loads(request.body)
        return HttpResponseRedirect("http://127.0.0.1:9000/#/welcome-profile")


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        email, uuid, password = '', '', ''
        if 'email' in request.data:
            email = request.data['email']
        if 'uuid' in request.data:
            uuid = request.data['uuid']
            try:
                register_email = RegisterEmail.objects.get(uuid=uuid)
                email = register_email.email
            except ObjectDoesNotExist:
                return Response({'details': 'Invalid User Register.'}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        data = {'email': email, 'password': password}
        try:
            user = KnackUser.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            user = KnackUser.objects.create_user(data['email'], data['password'])

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_online = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            #avatar = get_thumbnail(user.picture, '40x40', crop='center')
            #avatar_url = None
            #if avatar:
            #    avatar_url = avatar.url
            return Response({'token': token.key,
                             'id': user.id,
                             'full_name': user.full_name,
                             'age': user.age,
                             'picture': ''
                             })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = ObtainAuthToken.as_view()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    serialized = ChangePasswordSerializer(data = request.data)
    if serialized.is_valid():
        data = {field: data for (field, data) in request.data.items()}
        token = data['token']
        tokenObj = Token.objects.get(key=token)
        user = tokenObj.user

        if check_password(data['current_password'], user.password):
            user.set_password(data['password'])
            user.save()
            return Response({'details':['Success password changed']}, status=status.HTTP_200_OK)
        else:
            return Response({'current_password':['Wrong current password']}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def forgot_password(request):
    serialized = ForgotPasswordSerializer(data=request.data)
    if serialized.is_valid():
        email = request.data['email']

        date = timezone.now().strftime('%b %dth, %Y')
        try:
            object = RegisterEmail.objects.get(email=email)
            guid = object.uuid
        except ObjectDoesNotExist:
            guid = uuid.uuid4().hex
            # save register email
            object = RegisterEmail(email=email, uuid=guid)
            object.save()

        subject = 'Password Reset!'
        plaintext = get_template('reset_email.txt')
        htmly = get_template('reset_email.html')
        context = ({'date': date, 'uuid': guid})

        text_content = plaintext.render(context)
        html_content = htmly.render(context)

        msg = EmailMultiAlternatives(subject, text_content, 'arnokuhlein@gmail.com', [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # send_mail(subject, message, 'noreply@unacks.com', [serialized['email']])
        return Response({'email': email}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def reset_password(request):
    uuid = request.data['uuid']
    password = request.data['password']
    try:
        object = RegisterEmail.objects.get(uuid=uuid)
        user = User.objects.get(email=object.email)
    except ObjectDoesNotExist:
        return Response({'details': ['User does not exist.']}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(password)
    user.save()
    return Response({'details': ['Success password changed']}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    SOCIAL_BACKENDS = {
        FacebookOAuth2.name: FacebookOAuth2
    }

    def retrieve(self, request, pk=None):
        profile_id = request.GET.get('user_id', None)
        public_url = request.GET.get('public_url', None)
        social_backend = request.GET.get('social_backend', None)
        social_code = request.GET.get('social_code', None)
        if public_url:
            user = get_object_or_404(self.queryset, username=public_url)
        elif profile_id:
            user = get_object_or_404(self.queryset, pk=int(profile_id))
        elif request.user.id:
            user = get_object_or_404(self.queryset, pk=request.user.id)
        elif social_backend and social_code:
            code = Code.get_code(social_code)
            account = KnackUser.objects.get(email=code.email)
            backend_class = self.SOCIAL_BACKENDS.get(social_backend)
            account.backend = '{0}.{1}'.format(backend_class.__module__, backend_class.__name__)

            token, created = Token.objects.get_or_create(user=account)
            avatar = get_thumbnail(account.picture, '40x40', crop='center')
            avatar_url = None
            if avatar:
                avatar_url = avatar.url
            return Response({'token': token.key,
                             'id': account.id,
                             'full_name': account.full_name,
                             'college': account.college,
                             'age': account.age,
                             'picture': account.picture})
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if not hasattr(user, 'sociallink'):
            sociallink = SocialLink(user=user, twitter='', facebook='', instagram='', googleplus='')
            sociallink.save()
            user.sociallink = sociallink

        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class UserAlreadyRegistered(viewsets.GenericViewSet):
    serializer_class = AuthTokenSerializer

    def retrieve(self, request, pk=None):
        guid = request.GET.get('uuid', None)
        try:
            register_email = RegisterEmail.objects.get(uuid=guid)
            email = register_email.email
            try:
                user = KnackUser.objects.get(email=email)
                data = {'email': user.email, 'password': user.password}
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    user = serializer.validated_data['user']
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key,
                                     'id': user.id,
                                     'full_name': user.full_name,
                                     'age': user.age,
                                     'picture': ''
                                     })
            except ObjectDoesNotExist:
                return Response({'details': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'details': 'Invalid Register'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetable(viewsets.GenericViewSet):

    def retrieve(self, request, pk=None):
        guid = request.GET.get('uuid', None)
        try:
            register_email = RegisterEmail.objects.get(uuid=guid)
            email = register_email.email
            return Response({'email': email, 'uuid': register_email.uuid})
        except ObjectDoesNotExist:
            return Response({'details': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class UserEditViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        full_name = request.data['full_name'].split(' ')
        first_name = full_name[0]
        try:
            last_name = full_name[1]
        except:
            last_name = ''
        instance.first_name = first_name
        instance.last_name = last_name

        if not instance.username and request.data['full_name'] != '':
            username = first_name.lower() + '_' + last_name.lower()
            i = 0
            while True:
                if self.queryset.filter(username=username):
                    username += str(i)
                    i += 1
                else:
                    instance.username = username
                    break

        if request.data['year'] != 'null':
            year = Year.objects.get_or_create(name=request.data['year'])
            instance.year = year[0]

        if request.data['college'] != 'null':
            college = College.objects.get_or_create(name=request.data['college'])
            instance.college = college[0]

        if request.data['age'] != 'null':
            instance.age = request.data['age']

        if request.data['gender'] != 'null':
            instance.gender = request.data['gender']

        instance.save()

        serializer = ProfileSerializer(instance)
        return Response(serializer.data)


class UserPictureEditViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        picture = save_to_image(instance, request.data['picture'])
        instance.picture = picture
        instance.save()

        serializer = ProfileSerializer(instance)
        return Response(serializer.data)


class UserSocialEditViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.sociallink.twitter = request.data['twitter']
        instance.sociallink.facebook = request.data['facebook']
        instance.sociallink.instagram = request.data['instagram']
        instance.sociallink.googleplus = request.data['googleplus']
        instance.sociallink.save()
        return Response({'result': 'success'})


class UserAboutEditViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.about_me = request.data['about']
        instance.save()
        return Response({'result': 'success'})


class UserPaymentEditViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.payment_venmo = request.data['venmo']
        instance.payment_paypal = request.data['paypal']
        instance.save()
        return Response({'result': 'success'})


class UserUrlEditViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        public_profile_url = request.data['public_url']
        username = public_profile_url.split(r'/')[-1]
        users = KnackUser.objects.filter(username=username).exclude(pk=instance.pk)
        if len(users) > 0:
            return Response({'detail': 'Already exists'}, status=status.HTTP_400_BAD_REQUEST)
        instance.username = username
        instance.save()
        return Response({'result': 'success'})


class UserReasonsViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        d = dict(six.iterlists(request.data))
        reasons = []
        for key, value in sorted(six.iteritems(d)):
            reasons.append(value[0])
        instance.reasons = reasons
        instance.save()
        return Response({'result': 'success'})


class UserNotificationEmailViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        if self.request.user.id:
            user = get_object_or_404(self.queryset, pk=self.request.user.id)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.notification_email = request.data['notification_email']
        instance.save()
        return Response({'result': 'success'})


class CollegeListView(APIView):

    def get(self, request, format=None):
        """
        Return a list of all colleges.
        """
        colleges = College.objects.values('name')
        return Response({'results': colleges})


class YearListView(APIView):

    def get(self, request, format=None):
        """
        Return a list of all years.
        """
        years = Year.objects.values('name')
        return Response({'results': years})


class GenderListView(APIView):

    def get(self, request, format=None):
        """
        Return a list of all genders.
        """
        return Response({'results': KnackUser.GENDER_CHOICES})


class UserConnectView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        pk = request.GET.get('id', 0)
        current_user = request.user
        user_to_connect = User.objects.get(pk=pk)
        if user_to_connect not in current_user.connections.all() and user_to_connect.pk != current_user.pk:
            Notification.objects.create(user=user_to_connect, sender=current_user, type=Notification.TYPE_CONNECTION)
            current_user.connections.add(user_to_connect)

        return Response({'result': 'success'})


class UserDisconnectView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        pk = request.GET.get('id', 0)
        current_user = request.user
        user_to_disconnect = User.objects.get(pk=pk)
        if user_to_disconnect in current_user.connections.all() and user_to_disconnect.pk != current_user.pk:
            current_user.connections.remove(user_to_disconnect)

        return Response({'result': 'success'})


profile_view = UserViewSet.as_view({'get': 'retrieve'})
already_registered = UserAlreadyRegistered.as_view({'get': 'retrieve'})
isResetable = PasswordResetable.as_view({'get': 'retrieve'})
profile_edit_view = UserEditViewSet.as_view({'put': 'update'})
profile_picture_edit_view = UserPictureEditViewSet.as_view({'put': 'update'})
profile_social_edit_view = UserSocialEditViewSet.as_view({'put': 'update'})
profile_about_edit_view = UserAboutEditViewSet.as_view({'put': 'update'})
profile_payment_edit_view = UserPaymentEditViewSet.as_view({'put': 'update'})
profile_url_edit_view = UserUrlEditViewSet.as_view({'put': 'update'})
profile_reasons_edit_view = UserReasonsViewSet.as_view({'put': 'update'})
college_list_view = CollegeListView.as_view()
year_list_view = YearListView.as_view()
gender_list_view = GenderListView.as_view()
