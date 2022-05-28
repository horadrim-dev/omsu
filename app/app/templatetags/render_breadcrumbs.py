from django import template

register = template.Library()

@register.inclusion_tag('app/breadcrumbs.html')
def render_breadcrumbs(bc_items:dict):
    url_chain = ''
    breadcrumbs_items = {'Главная':''}
    breadcrumbs_items.update(bc_items)

    for key, value in breadcrumbs_items.items():
        url_chain += value + '/'
        breadcrumbs_items[key] = url_chain

    context = {
        'breadcrumbs_items' : breadcrumbs_items
    }
    return context
