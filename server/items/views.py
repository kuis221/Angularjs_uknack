import django_filters
from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Item, Category
from . import serializers
from knacks.views import save_photos, ReadOnlyOrIsAdminUser, ConnectionsFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    paginate_by = 100
    permission_classes = (ReadOnlyOrIsAdminUser,)


class CustomFilterList(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            return qs.filter(**{'%s__%s' % (self.name, self.lookup_type): values})
        return qs


class ItemFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(name="owner__id", lookup_type='exact')
    min_age = django_filters.NumberFilter(name="owner__age", lookup_type='gte')
    max_age = django_filters.NumberFilter(name="owner__age", lookup_type='lte')
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    gender = django_filters.CharFilter(name="owner__gender", lookup_type='exact')
    college = django_filters.CharFilter(name="owner__college", lookup_type='exact')
    categories = CustomFilterList(name="category", lookup_type='in')
    connections_only = ConnectionsFilter(name="owner__connections", lookup_type='in')

    class Meta:
        model = Item
        fields = ['id', 'user_id', 'type', 'min_age', 'max_age', 'min_price', 'max_price', 'gender', 'categories',
                  'connections_only']

    def __init__(self, data=None, queryset=None, prefix=None, strict=None):
        data = data.copy()
        if hasattr(data, 'college') and data['college'] == '':
            data.pop('college', None)
        if hasattr(data, 'gender') and data['gender'] == '':
            data.pop('gender', None)
        super(ItemFilter, self).__init__(data, queryset, prefix, strict)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    PAGINATE_BY_PARAM = 'page_size'
    filter_class = ItemFilter

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
        Item.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        # Add one to instance views to display the correct value. Do not save the instance!
        instance.views += 1

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def check_object_permissions(self, request, obj):
        # Check if a user is an owner of the item if a request is not safe
        if request.method not in SAFE_METHODS and request.user != obj.owner:
            self.permission_denied(request)

        return super(ItemViewSet, self).check_object_permissions(request, obj)

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search_text = self.request.GET.get('search_text', None)
        queryset = super(ItemViewSet, self).get_queryset()

        if search_text:
            queryset = queryset.filter(Q(owner__first_name__icontains=search_text) |
                                       Q(owner__last_name__icontains=search_text) |
                                       Q(name__icontains=search_text) |
                                       Q(description__icontains=search_text))

        if sort_by:
            queryset = queryset.order_by('-modified_at')
        return queryset
