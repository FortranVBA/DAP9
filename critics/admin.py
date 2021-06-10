"""Project OC DAP 9 - Critics admin file."""

from django.contrib import admin
from .models import Review

# Register your models here.
admin.site.register(Review)
