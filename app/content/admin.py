from django.contrib import admin
from .models import Post, Feed, Attachment
# Register your models here.

class AttachmentInline(admin.TabularInline):
    model = Attachment
    exclude = ['extension']
    readonly_fields = ('hits',)

class PostAdmin(admin.ModelAdmin):
    # view_on_site = True
    # date_hierarchy = 'publish_date'
    # list_display = (
    #     'title', 'alias', 'menu', 'feed', 'text'
    # )
    # list_filter = ('is_draft', 'issue_type',)
    # search_fields = (
    #     'title', 'short_description',
    #     'posts__title', 'posts__short_description',
    # )
    # readonly_fields = ('hits',)
    # sortable_by = ('issue_number', 'publish_date',)
    save_as = True
    inlines = (AttachmentInline,)

    # actions = ('publish_issues', 'make_draft',)

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