from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import Section, Column, Module, ModuleContent
from django import forms
import uuid
# Register your models here.

class ColumnInline(admin.TabularInline):
    model = Column
    exclude = []

class ModuleContentInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(ModuleContentInlineFormSet, self).clean()

        for form in self.forms:
            if not form.is_valid():
                return #other errors exist, so don't bother
            if form.cleaned_data:
                if form.cleaned_data.get('content_type') == 'menu' and not form.cleaned_data.get('menu'):
                    raise ValidationError('Поле "Меню" обязательно для заполнения!');
                if form.cleaned_data.get('content_type') == 'feed' and not form.cleaned_data.get('feed'):
                    raise ValidationError('Поле "Лента постов" обязательно для заполнения!');
                if form.cleaned_data.get('content_type') == 'post' and not form.cleaned_data.get('post'):
                    raise ValidationError('Поле "Пост" обязательно для заполнения!');
            #     total += form.cleaned_data['cost']
            # assert False, form.cleaned_data
        #compare only if Item inline forms were clean as well
        # if self.instance.__total__ is not None and self.instance.__total__ != total:
        #     raise ValidationError('Oops!')

class ModuleContentInline(admin.StackedInline):
    model = ModuleContent
    exclude = []
    extra = 0
    formset = ModuleContentInlineFormSet
    class Media:
        js = ('grid/js/modulecontent.js',)

    

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

    inlines = (ModuleContentInline, )

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