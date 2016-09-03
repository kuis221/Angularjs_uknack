import re
import base64
import uuid
from time import time

import django_filters
from django.db.models import Q, F
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import login, get_user_model
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from social.apps.django_app.default.models import Code
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from rest_framework.permissions import SAFE_METHODS, BasePermission
from social.backends.facebook import FacebookOAuth2

from .models import Knack, KnackIdea, Category
from . import serializers

SOCIAL_BACKENDS = {
    FacebookOAuth2.name: FacebookOAuth2
}
User = get_user_model()


class ReadOnlyOrIsAdminUser(BasePermission):
    """
    Allows not safe access only to admin users.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            (request.user and request.user.is_staff)
        )


def save_photos(data, instance=None):
    for i in range(5):
        photo = data['photo%s' % i]
        if instance:
            instance_photo = getattr(instance, 'photo%s' % i, None)
            if instance_photo:
                if photo.endswith(instance_photo.url):
                    data['photo%s' % i] = instance_photo
                    continue

        if re.search(r"data:[\w/\-\.]+;\w+,.*", photo) is not None:
            try:
                filename = '%s_%s.png' % (i, uuid.uuid4())
                binary_data = base64.b64decode(photo[photo.index(",") + 1:])
                data['photo%s' % i] = ContentFile(binary_data, filename)
            except (IOError, OSError) as e:
                # TODO: log here
                print(e)
                data['photo%s' % i] = None
        else:
            data['photo%s' % i] = None


def fb_login(request):
    context = RequestContext(request, {'user': request.user})
    backend_name = 'facebook'
    backend_class = SOCIAL_BACKENDS.get(backend_name)
    request.user.backend = '{0}.{1}'.format(backend_class.__module__, backend_class.__name__)
    if request.user is not None:
        if request.user.is_active:
            login(request, request.user)

    if backend_name:
        response = HttpResponseRedirect("/#/private-profile")
        code = Code.make_code(request.user.email)
        token, created = Token.objects.get_or_create(user=request.user)
        response.set_cookie('social_code', code.code)
        response.set_cookie('social_backend', backend_name)
        response.set_cookie('token', token.key)
        return response
    else:
        response = HttpResponseRedirect("/#/")
        return response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    paginate_by = 100
    permission_classes = (ReadOnlyOrIsAdminUser, )


class CustomFilterList(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            return qs.filter(**{'%s__%s' % (self.name, self.lookup_type): values})
        return qs


class ConnectionsFilter(django_filters.Filter):
    def filter(self, qs, value):
        value = int(value)
        if value:
            user = User.objects.get(pk=value)
            connections = [u.pk for u in user.connections.all()]
            return qs.filter(owner__id__in=connections)
        return qs


class KnackFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(name="owner__id", lookup_type='exact')
    min_age = django_filters.NumberFilter(name="owner__age", lookup_type='gte')
    max_age = django_filters.NumberFilter(name="owner__age", lookup_type='lte')
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    gender = django_filters.CharFilter(name="owner__gender", lookup_type='exact')
    college = django_filters.CharFilter(name="owner__college__name", lookup_type='iexact')
    year = django_filters.CharFilter(name="owner__year__name", lookup_type='iexact')
    categories = CustomFilterList(name="category", lookup_type='in')
    connections_only = ConnectionsFilter(name="owner__connections", lookup_type='in')

    class Meta:
        model = Knack
        fields = ['id', 'user_id', 'type', 'min_age', 'max_age', 'min_price', 'max_price', 'gender', 'college', 'year',
                  'categories', 'connections_only']

    def __init__(self, data=None, queryset=None, prefix=None, strict=None):
        data = data.copy()
        if hasattr(data, 'college') and data['college'] == '':
            data.pop('college', None)
        if hasattr(data, 'gender') and data['gender'] == '':
            data.pop('gender', None)
        super(KnackFilter, self).__init__(data, queryset, prefix, strict)


class KnackViewSet(viewsets.ModelViewSet):
    queryset = Knack.objects.all()
    serializer_class = serializers.KnackSerializer
    PAGINATE_BY_PARAM = 'page_size'
    filter_class = KnackFilter

    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        data = request.data

        save_photos(data)

        if data['willing_to_travel'] == 'true':
            data['willing_to_travel'] = True
        else:
            data['willing_to_travel'] = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def check_object_permissions(self, request, obj):
        # Check if a user is the owner of the knack if a request is not safe
        if request.method not in SAFE_METHODS and request.user != obj.owner:
            self.permission_denied(request)

        return super(KnackViewSet, self).check_object_permissions(request, obj)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        save_photos(data, instance)

        if data['willing_to_travel'] == 'true':
            data['willing_to_travel'] = True
        else:
            data['willing_to_travel'] = False

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # Override the method to count views
        instance = self.get_object()

        # This will hit db only once and will not trigger signals -> will not update modified_at field
        instance.__class__.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        # Add one to instance views to display the correct value. Do not save the instance!
        instance.views += 1

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search_text = self.request.GET.get('search_text', None)
        queryset = super(KnackViewSet, self).get_queryset()

        if search_text:
            queryset = queryset.filter(Q(owner__first_name__icontains=search_text) |
                                       Q(owner__last_name__icontains=search_text) |
                                       Q(name__icontains=search_text) |
                                       Q(description__icontains=search_text))

        queryset = queryset.order_by('-modified_at')
        return queryset


class KnackIdeaFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(name="owner_id", lookup_type='exact')
    min_age = django_filters.NumberFilter(name="owner__age", lookup_type='gte')
    max_age = django_filters.NumberFilter(name="owner__age", lookup_type='lte')
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    gender = django_filters.CharFilter(name="owner__gender", lookup_type='exact')
    college = django_filters.CharFilter(name="owner__college", lookup_type='iexact')
    categories = CustomFilterList(name="category", lookup_type='in')

    class Meta:
        model = KnackIdea
        fields = ['id', 'user_id', 'type', 'min_age', 'max_age', 'min_price', 'max_price', 'gender', 'categories']

    def __init__(self, data=None, queryset=None, prefix=None, strict=None):
        data = data.copy()
        if hasattr(data, 'college') and data['college'] == '':
            data.pop('college', None)
        if hasattr(data, 'gender') and data['gender'] == '':
            data.pop('gender', None)
        super(KnackIdeaFilter, self).__init__(data, queryset, prefix, strict)


class KnackIdeaViewSet(viewsets.ModelViewSet):
    queryset = KnackIdea.objects.all()
    serializer_class = serializers.KnackIdeaSerializer
    PAGINATE_BY_PARAM = 'page_size'
    permission_classes = (ReadOnlyOrIsAdminUser,)
    # filter_class = KnackIdeaFilter
    # filter_class = KnackIdeaFilter

    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super(KnackIdeaViewSet, self).get_queryset()
        queryset = queryset.order_by('-modified_at')
        return queryset


class MilesListView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all colleges.
        """
        return Response({'results': Knack.miles_choices})


class ChargeListView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all charges.
        """
        return Response({'results': Knack.charge_choices})


class TypesListView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all knack types.
        """
        return Response({'results': Knack.KNACK_TYPES})


miles_list_view = MilesListView.as_view()
charge_list_view = ChargeListView.as_view()
types_list_view = TypesListView.as_view()
