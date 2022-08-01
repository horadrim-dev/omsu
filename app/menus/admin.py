from django.contrib import admin, messages

from django import forms
# Register your models here.
from .forms import AdminMenuForm
from .models import Menu 
from content.models import ExtraContent

class ExtraContentInline(admin.StackedInline):
    model = ExtraContent
    fk_name = 'tied_to_menu'
    exclude = []
    extra = 0
    # readonly_fields = ('hits',)

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        # fields = []
        exclude = []
# @admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    # поле alias будет автоматически заполнено на основе заголовка
    # prepopulated_fields = {
    #     "alias" : ("title",)
    # 
    form = MenuForm
    list_display = ('leveled_title', 'id', 'alias', 'url', 'short_description','list_order', 'order', 'level', )
    fieldsets = (
        ('Общее', {
            'fields': ('title', 'alias', 'parent', 'published', 'megamenu', 'icon', 'short_description', 'description',)
        }),
        ('Контент', {
                'fields': ('content_type', 'content_post', 
                        'content_feed', 'feed_style', 'feed_num_columns', 'feed_count_items', 'feed_readmore', 'feed_sort_direction',
                        'content_menu', 'menu_style')
                # 'fields':('content_layout',)
        }),
    )
    inlines = (ExtraContentInline, )

    # def get_form(self, request, obj=None, **kwargs):
    #     if request.user.is_superuser:
    #         kwargs['form'] = AdminMenuForm
    #     return super().get_form(request, obj, **kwargs)
    def save_model(self, request, obj, form, change):
        # if 'alias' in form.changed_data:
        #     if obj.title == 'Главная':
        #         messages.add_message(request, messages.ERROR, 'Менять меню "Главная" запрещено.')
        #         return False
        # if 'title' in form.changed_data:
        #     if obj.alias == 'home':
        #         messages.add_message(request, messages.ERROR, 'Менять меню "Главная" запрещено.')
        #         return False
        
        super().save_model(request, obj, form, change)

admin.site.register(Menu, MenuAdmin)