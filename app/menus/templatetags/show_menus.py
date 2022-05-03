from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/block_menus.html')
def show_menus(parent=None):
    context = {}

    if parent:
        category = Menu.objects.get(alias = parent)
        menus = Menu.objects.filter(parent_id = category.id)
    else:
        category = None
        menus = Menu.objects.filter(parent_id__isnull=True)

    context['only_html'] = True
    context['category'] = category
    context['menus'] = menus

    return context
