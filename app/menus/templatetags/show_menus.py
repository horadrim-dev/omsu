from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/show_menus.html')
def show_menus():
    return {'menus':Menu.objects.all()}
