from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/render_menus.html')
def render_menus(section=None, parent=None):
    context = {}

    if section:
        alias = parent if parent else section
            
        page = Menu.objects.get(alias = alias)
        menus = Menu.objects.filter(parent_id = page.id)
    else:
        page = None
        menus = Menu.objects.filter(level=1)

    context['from_module'] = True
    context['section'] = section
    context['page'] = page
    context['menus'] = menus

    return context
