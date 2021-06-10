"""Project OC DAP 9 - Follow admin file."""

from django.contrib import admin
from .models import UserFollows

# Register your models here.
admin.site.register(UserFollows)
