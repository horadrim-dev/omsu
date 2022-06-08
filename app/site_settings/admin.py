from django.contrib import admin, messages
from .models import Section, Column, Module
from django import forms
import uuid
# Register your models here.

class ColumnInline(admin.TabularInline):
    model = Column
    exclude = []
    # readonly_fields = ('hits',)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    inlines = (ColumnInline, )

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        # fields = []
        exclude = []

class ModuleAdmin(admin.ModelAdmin):
    form = ModuleForm
    list_display = ['name', 'published', 'column', 'order', 'id']
    list_filter = ('published', 'menu', 'column',)
    search_fields = ('title', )
    readonly_fields = ('id', )
    actions = ('publish', 'unpublish', 'duplicate')

    def publish(self, request, queryset):
        queryset.update(published=True)
        message = str(len(queryset)) + ' модуль(ей) опубликован(ы)'
        messages.add_message(request, messages.SUCCESS, message)
    publish.short_description = 'Опубликовать'

    def unpublish(self, request, queryset):
        queryset.update(published=False)
        message = str(len(queryset)) + ' модуль(ей) снят(ы) с публикации'
        messages.add_message(request, messages.SUCCESS, message)
    unpublish.short_description = 'Снять с публикации'

    def duplicate(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.name += ' (Копия - {})'.format(uuid.uuid4())
            obj.published = False
            obj.save()
        message = str(len(queryset)) + ' модуль(ей) успешно скопирован(ы)'
        messages.add_message(request, messages.SUCCESS, message)
    duplicate.short_description = 'Дублировать'

admin.site.register(Section, SectionAdmin)
admin.site.register(Module, ModuleAdmin)