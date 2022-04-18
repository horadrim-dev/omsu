from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/show_menus.html')
def show_menus():

    menus = Menu.objects.filter(parent_id__isnull=True)

    context = {
        'add_path': True,
        'category': None,
        'menus': menus
    }
    return context
