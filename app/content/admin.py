from django.contrib import admin
from .models import Post, Feed, Attachment
import uuid
# Register your models here.

class AttachmentInline(admin.TabularInline):
    model = Attachment
    exclude = ['extension']
    readonly_fields = ('hits',)

class PostAdmin(admin.ModelAdmin):
    # view_on_site = True
    # date_hierarchy = 'publish_date'
    list_display = (
        'title', 'published', 'published_at', 'created_at',
        'menu', 'feed', 'id',
    )
    list_filter = ('published', 'menu', 'feed',)
    search_fields = (
        'title', 'published_at', 'created_at'
        # 'title', 'short_description',
        # 'posts__title', 'posts__short_description',
    )
    readonly_fields = ('id', 'created_at', 'hits')
    # sortable_by = ('issue_number', 'publish_date',)
    save_as = True
    inlines = (AttachmentInline,)

    actions = ('publish', 'unpublish', 'duplicate')
    def publish(self, reguest, queryset):
        queryset.update(published=True)
    publish.short_description = 'Опубликовать'

    def unpublish(self, reguest, queryset):
        queryset.update(published=False)
    unpublish.short_description = 'Снять с публикации'

    def duplicate(self, reguest, queryset):
        for obj in queryset:
            obj.id = None
            obj.title += ' (Копия - {})'.format(uuid.uuid4())
            obj.save()
    duplicate.short_description = 'Дублировать'
        # def publish_issues(self, request, queryset):
    #     updated = queryset.update(is_draft=False)
    #     messages.add_message(
    #         request,
    #         messages.SUCCESS,
    #         f'Successfully published {updated} issue(s)',
    #     )

    # publish_issues.short_description = 'Publish issues now'

admin.site.register(Post, PostAdmin)
admin.site.register(Feed)