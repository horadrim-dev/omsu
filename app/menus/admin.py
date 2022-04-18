from django.contrib import admin

# Register your models here.

from .models import Menu, Page

admin.site.register(Menu)
admin.site.register(Page)
