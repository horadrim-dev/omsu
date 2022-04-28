from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/menubar.html')
def render_menubar(maxlevel=2):
    context = {'items': [0,0]}

    # menus = Menu.objects.filter(

    # )
    
    return context
