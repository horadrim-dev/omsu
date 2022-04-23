from django.contrib import admin

# Register your models here.

from .models import Menu, Page

admin.site.register(Page)

admin.site.register(Menu)

# @admin.register(Menu)
# class MenuAdmin(admin.ModelAdmin):
#     # поле alias будет автоматически заполнено на основе заголовка
#     prepopulated_fields = {
#         "alias" : ("title",)
#     }