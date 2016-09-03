from django import forms
from django.contrib import admin
from redactor.widgets import RedactorEditor

from . import models


class KnackIdeaImageAdmin(admin.ModelAdmin):
    pass


class KnackIdeaImageInline(admin.StackedInline):
    model = models.KnackIdeaImage
    max_num = 5
    extra = 0


class KnackIdeaAdminForm(forms.ModelForm):
    class Meta:
        model = models.KnackIdea
        fields = '__all__'
        widgets = {
            'business_model': RedactorEditor()
        }


class KnackIdeaAdmin(admin.ModelAdmin):
    inlines = [KnackIdeaImageInline, ]
    form = KnackIdeaAdminForm


admin.site.register(models.Knack)
admin.site.register(models.Category)
admin.site.register(models.KnackIdea, KnackIdeaAdmin)
