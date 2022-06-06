from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/render_menu.html')
def render_menu(parent=None):
    context = {}

    # if section:
        # alias = parent if parent else section
            
    page = Menu.objects.get(alias = parent)
    menus = Menu.objects.filter(parent_id = page.id)
    # else:
    #     page = None
    #     menus = Menu.objects.filter(level=1)

    context['from_module'] = True
    # context['section'] = section
    context['page'] = page
    context['menus'] = menus

    return context
