from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/show_menus.html')
def show_menus(parent=None):
    context = {}

    if parent:
        page = Menu.objects.get(alias = parent)
        menus = Menu.objects.filter(parent_id = page.id)
    else:
        page = None
        menus = Menu.objects.filter(parent_id__isnull=True)

    context['add_path'] = True
    context['page'] = page
    context['menus'] = menus

    return context
