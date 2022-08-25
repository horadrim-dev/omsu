from turtle import position
from django.contrib import admin,  messages
from .models import Post, Feed, Attachment, ExtraContent, Tag
from .forms import ExtraContentForm, PostForm
import uuid
from django import forms
# Register your models here.

class AttachmentInline(admin.TabularInline):
    model = Attachment
    exclude = ['extension']
    readonly_fields = ('hits',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


class PostAdmin(admin.ModelAdmin):
    # view_on_site = True
    # date_hierarchy = 'publish_date'
    form = PostForm
    list_display = (
        'title', 'published', 'published_at', 
        'feed', 'id',
    )
    list_filter = ('published', 'feed',)
    search_fields = ('title', )
    readonly_fields = ('id', 'hits')
    # sortable_by = ('issue_number', 'publish_date',)
    save_as = True
    inlines = (AttachmentInline,)

    actions = ('publish', 'unpublish', 'duplicate')

    def publish(self, request, queryset):
        queryset.update(published=True)
        message = str(len(queryset)) + ' элемент(ов) опубликован(ы)'
        messages.add_message(request, messages.SUCCESS, message)
    publish.short_description = 'Опубликовать'

    def unpublish(self, request, queryset):
        queryset.update(published=False)
        message = str(len(queryset)) + ' элемент(ов) сняты с публикации'
        messages.add_message(request, messages.SUCCESS, message)
    unpublish.short_description = 'Снять с публикации'

    def duplicate(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.title += ' (Копия - {})'.format(uuid.uuid4())
            obj.published = False
            obj.save()
        message = str(len(queryset)) + ' элемент(ов) успешно скопирован(ы)'
        messages.add_message(request, messages.SUCCESS, message)
    duplicate.short_description = 'Дублировать'


    def save_model(self, request, obj, form, change):
        # assert False, (form.has_changed(), form.changed_data)
        # messages.add_message(request, messages.INFO, 'changed_data = ' + str(form.changed_data))
        # assert False, (obj)
        if ('menu' in form.changed_data) or ('feed' in form.changed_data):
            # assert False, (form.cleaned_data,'||||', form.changed_data)
            num = obj.relocate_attachments()#form.cleaned_data.menu)
            message = 'Ссылки на {} файл(а) обновлены.'.format(num)
            messages.add_message(request, messages.INFO, message)

        # if 'feed' in form.changed_data:
        # assert False, (
        #     form.data,'<br><br>////////', 
        #     form.cleaned_data, '<br><br>//////',
        #     form.changed_data, '<br><br>//////',
        #     obj.title, '//////',
        #     )
        # assert False, form.changed_data

        super().save_model(request, obj, form, change)

        # def publish_issues(self, request, queryset):
    #     updated = queryset.update(is_draft=False)
    #     messages.add_message(
    #         request,
    #         messages.SUCCESS,
    #         f'Successfully published {updated} issue(s)',
    #     )

    # publish_issues.short_description = 'Publish issues now'

class ExtraContentAdmin(admin.ModelAdmin):
    form = ExtraContentForm
    list_display = (
        'tied_to_menu', 'position', 'content_type', 'id'
    )
    list_filter = ('tied_to_menu', 'content_type', 'position',)


admin.site.register(Post, PostAdmin)
admin.site.register(Feed)
# admin.site.register(Tag, TagAdmin)
admin.site.register(ExtraContent, ExtraContentAdmin)