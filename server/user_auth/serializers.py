import json

import six
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from user_auth.models import Feedback, SocialLink, Description, RegisterEmail, College, Year

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(write_only=True)
    # birthday = serializers.DateField(write_only=True)

    class Meta:
        model = User
        # fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'birthday')
        fields = ('email', 'password')
        # write_only_fields = ('password', )

    def validate_email(self, value):
        domain = value.split('@')[1]
        if domain[-4:] != '.edu':
            raise serializers.ValidationError("Email must be .edu email.")
        return value
    # def validate(self, data):
    #     password1 = data['password']
    #     password2 = data['password2']
    #     if password1 and password2 and password1 != password2:
    #         raise serializers.ValidationError('The two passwords do not match.')
    #     return data


class RegisterEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisterEmail
        fields = ('email',)

    def validate_email(self, value):
        domain = value.split('@')[1]
        if domain[-4:] != '.com':
            raise serializers.ValidationError("Please enter a valid .edu email.")
        return value

    def validate(self, attrs):
        try:
            object = RegisterEmail.objects.get(email=attrs['email'])
            raise serializers.ValidationError("An account is already associated with this email")
        except ObjectDoesNotExist:
            return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'base_template': 'password.html'},
        required=False
    )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ReturnUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'id')


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)

    def restore_object(self, attrs, instance=None):
        email = attrs.pop('email', None)
        #obj = super(LogoutSerializer, self).restore_object(attrs, instance)
        obj = User.objects.get(email=email)
        return obj


class ChangePasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    current_password = serializers.CharField(
        style={'base_template': 'password.html'},
        required=False
    )
    password = serializers.CharField(
        style={'base_template': 'password.html'},
        required=False
    )
    password2 = serializers.CharField(
        style={'base_template': 'password.html'},
        required=False
    )

    def validate_token(self, token):
        token_array = Token.objects.filter(key=token)
        if token_array:
            return token
        else:
            raise serializers.ValidationError('User does not exist')

    def validate(self, data):
        password1 = data['password']
        password2 = data['password2']
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError('The two passwords do not match.')
        return data


class ForgotPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisterEmail
        fields = ('email',)

    def validate_email(self, value):
        domain = value.split('@')[1]
        if domain[-4:] != '.com':
            raise serializers.ValidationError("Please enter a valid .edu email.")
        return value

    def validate(self, attrs):
        try:
            object = User.objects.get(email=attrs['email'])
            return object
        except ObjectDoesNotExist:
            raise serializers.ValidationError('User does not exist')


class ResetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisterEmail
        fields = ('email',)

    def validate_email(self, value):
        domain = value.split('@')[1]
        if domain[-4:] != '.com':
            raise serializers.ValidationError("Please enter a valid .edu email.")
        return value

    def validate(self, attrs):
        try:
            object = User.objects.get(email=attrs['email'])
            return object
        except ObjectDoesNotExist:
            raise serializers.ValidationError('User does not exist')


class AuthTokenSerializer(serializers.Serializer):
    """
    Restfuls AuthTokenSerializer with modifications to use email rather than user
    """
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        exclude = ('id', 'user')


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        exclude = ('id', 'user')


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        exclude = ('id', 'user')


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        exclude = ('id', )


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        exclude = ('id', )


class BasicProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(source='sociallink', many=False)
    descriptions = DescriptionSerializer(source='description_set', many=True)
    feedbacks = FeedbackSerializer(source='feedback_set', many=True)
    full_name = serializers.CharField(max_length=255, required=True, allow_blank=True)
    college = serializers.ReadOnlyField(source='college.name')
    year = serializers.ReadOnlyField(source='year.name')
    picture = serializers.SerializerMethodField('get_avatar_thumbnail')
    last_seen = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'full_name', 'first_name', 'last_name', 'gender', 'age', 'college', 'year', 'picture',
                  'feedbacks', 'grand_total', 'reasons', 'about_me', 'payment_venmo', 'payment_paypal', 'username',
                  'created_at', 'last_seen', 'social_links', 'descriptions', 'id', 'is_online', 'connections',
                  'notification_email')

    def __init__(self, *args, depth=2, with_connections=True, **kwargs):
        if depth > 0 and with_connections:
            depth -= 1
            self.fields['connections'] = BasicProfileSerializer(depth=depth, with_connections=with_connections,
                                                                many=True, read_only=True)

        super(BasicProfileSerializer, self).__init__(*args, **kwargs)

    def get_avatar_thumbnail(self, obj):
        if obj.picture:
            return get_thumbnail(obj.picture, '100x100', crop='center').url
        else:
            return None

    def get_last_seen(self, obj):
        mins = (timezone.now() - obj.last_seen).total_seconds() // 60
        if mins >= 1440:
            mins = int(mins) // 1440
            unit = ' days ago'
        elif mins >= 60:
            mins = int(mins) // 60
            unit = ' hours ago'
        else:
            mins = int(mins)
            unit = ' minutes ago'
        return str(mins) + unit

    def get_created_at(self, obj):
        return obj.created_at.strftime('%b %dth, %Y')

    def update(self, instance, validated_data):
        instance.age = validated_data.get('age')
        full_name = validated_data.get('full_name').split(' ')
        instance.first_name = full_name[0]
        try:
            instance.last_name = full_name[1]
        except:
            instance.last_name = ''
        # instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

    def to_internal_value(self, data):
        picture = data.pop('picture')[0]
        if not isinstance(picture, str) or not isinstance(picture, six.text_type):
            self.instance.picture = picture

        sociallinks = json.loads(data.pop('social_links', None)[0])
        if sociallinks:
            if not hasattr(self.instance, 'sociallink'):
                self.instance.sociallink = SocialLink()
            self.instance.sociallink.twitter = sociallinks['twitter']
            self.instance.sociallink.instagram = sociallinks['instagram']
            self.instance.sociallink.facebook = sociallinks['facebook']
            self.instance.sociallink.googleplus = sociallinks['googleplus']
            self.instance.sociallink.save()

        self.instance.description_set.all().delete()
        descriptions = json.loads(data.pop('descriptions', None)[0])
        for desc in descriptions:
            desc_obj = Description(description=desc['description'], user=self.instance)
            desc_obj.save()

        ret = super(BasicProfileSerializer, self).to_internal_value(data)
        return ret


class ProfileSerializer(BasicProfileSerializer):
    class Meta(BasicProfileSerializer.Meta):
        pass

    def __init__(self, *args, **kwargs):
        # Lazy loading, solving circular import errors
        from knacks.serializers import KnackSerializer
        from items.serializers import ItemSerializer

        self.fields['knacks'] = KnackSerializer(many=True, read_only=True, depth=-1)
        self.fields['items'] = ItemSerializer(many=True, read_only=True, depth=-1)

        super(ProfileSerializer, self).__init__(*args, **kwargs)


class PublicProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(source='sociallink', many=False, read_only=True)
    descriptions = DescriptionSerializer(source='description_set', many=True, read_only=True)
    picture = serializers.SerializerMethodField('get_avatar_thumbnail', read_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    college = serializers.ReadOnlyField(source='college.name')

    class Meta:
        model = User
        fields = ('email', 'full_name', 'age', 'college', 'picture',
                  'social_links', 'descriptions', 'id', 'is_online')

    def get_avatar_thumbnail(self, obj):
        if obj.picture:
            return get_thumbnail(obj.picture, '100x100', crop='center').url
        else:
            return None
