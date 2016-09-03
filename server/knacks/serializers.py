from django.contrib.auth import get_user_model
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from .models import Knack, KnackIdea, Category
from user_auth.serializers import BasicProfileSerializer

User = get_user_model()


class KnackSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    photos = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()

    class Meta:
        model = Knack
        exclude = ('deleted', 'video')

    def __init__(self, *args, depth=1, **kwargs):
        super(KnackSerializer, self).__init__(*args, **kwargs)
        if depth >= 0:
            self.fields['owner'] = BasicProfileSerializer(depth=depth, read_only=True)

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d/%y')

    def get_modified_at(self, obj):
        return obj.modified_at.strftime('%m/%d/%y')

    def get_photos(self, obj):
        photos = []
        if obj.photo0:
            photos.append(obj.photo0.url)
        if obj.photo1:
            photos.append(obj.photo1.url)
        if obj.photo2:
            photos.append(obj.photo2.url)
        if obj.photo3:
            photos.append(obj.photo3.url)
        if obj.photo4:
            photos.append(obj.photo4.url)
        return photos

    def get_thumbnails(self, obj):
        photos = []
        if obj.photo0:
            photos.append(obj.photo0.path)
        if obj.photo1:
            photos.append(obj.photo1.path)
        if obj.photo2:
            photos.append(obj.photo2.path)
        if obj.photo3:
            photos.append(obj.photo3.path)
        if obj.photo4:
            photos.append(obj.photo4.path)
        thumbs = []
        for photo in photos:
            thumbs.append(get_thumbnail(photo, '220x148', crop='center').url)
        return thumbs


class KnackIdeaSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    photos = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    # how_charge = serializers.SerializerMethodField()

    def get_how_charge(self, obj):
        return 'FLAT' if obj.how_charge == 'Flat Fee' else 'HR'

    class Meta:
        model = KnackIdea

    def get_photos(self, obj):
        return [image.photo.url for image in obj.knackideaimage_set.all()]

    def get_thumbnails(self, obj):
        arr = []
        photos = obj.knackideaimage_set.all()
        for item in photos:
            arr.append(get_thumbnail(item.photo, '219x147', crop='center').url)
        return arr


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
