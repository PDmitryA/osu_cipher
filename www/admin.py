from django.contrib import admin
from django.contrib.admin import register

from www.models import User, Score


@register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@register(Score)
class ScoresAdmin(admin.ModelAdmin):
    pass
