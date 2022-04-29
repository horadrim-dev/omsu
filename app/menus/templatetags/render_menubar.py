from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/menubar.html')
def render_menubar(maxlevel=2):
    '''Рендерит главное меню'''
    context = {}
    # получаем дерево меню, до 3 уровня (в шаблоне только 3, зачем больше?)
    context['menu_tree'] = Menu.get_subitems(parent=None, maxlevel=3)

    return context
