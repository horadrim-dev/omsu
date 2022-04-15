from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/show_menus.html')
def show_menus(pid = None, cat_slug = None):

    if cat_slug:
        category = Menu.objects.filter(alias = cat_slug)[0]
        menus = Menu.objects.filter(parent_id = category.id)
    else:
        if pid:
            category = Menu.objects.filter(id = pid)
            menus = Menu.objects.filter(parent_id = pid)
        else:
            menus = Menu.objects.filter(parent_id__isnull=True)
            category = None

    context = {
        'category': category,
        'menus': menus
    }
    return context
