from django.contrib import admin
from .models import AppUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(AppUser)
admin.site.register(Permission)
admin.site.register(ContentType)