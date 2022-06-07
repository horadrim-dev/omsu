from django.contrib import admin
from .models import Section, Column, Module
# Register your models here.

class ColumnInline(admin.TabularInline):
    model = Column
    exclude = []
    # readonly_fields = ('hits',)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    inlines = (ColumnInline, )

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'column', 'order']

admin.site.register(Section, SectionAdmin)
admin.site.register(Module, ModuleAdmin)