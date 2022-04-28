from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/menubar.html')
def render_menubar(maxlevel=2):
    context = {'maxlevel':maxlevel}

    
    
    return context
