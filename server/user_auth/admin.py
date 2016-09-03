from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import KnackUser, SocialLink, College, Year, RegisterEmail
from .forms import KnackUserChangeForm, KnackUserCreationForm


class SocialInline(admin.StackedInline):
    model = SocialLink


@admin.register(KnackUser)
class KnackUserAdmin(BaseUserAdmin):
    form = KnackUserChangeForm
    add_form = KnackUserCreationForm
    filter_horizontal = ('groups', 'user_permissions')
    inlines = (SocialInline, )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'age', 'picture')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_seen', 'is_online')}),
        (_('Uknack Information'), {'fields': ('college', 'year', 'reasons', 'about_me', 'username',
                                              'payment_venmo', 'payment_paypal')})
    )
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super(KnackUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(College)
admin.site.register(Year)
admin.site.register(RegisterEmail)
