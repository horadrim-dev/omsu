from django.contrib import admin
from .models import Section, Block
# Register your models here.

class BlockInline(admin.TabularInline):
    model = Block
    exclude = []
    # readonly_fields = ('hits',)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    inlines = (BlockInline, )

admin.site.register(Section, SectionAdmin)