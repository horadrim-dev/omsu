# from webbrowser import get
from django.shortcuts import render
# from django.http import JsonResponse
from . models import Menu
from content import views as content_views


def menus(request, parent=None, *args, **kwargs):

    if parent:
        current_alias = parent  # берем корневой элемент
    else:
        current_alias = list(kwargs.values())[-1]  # берем последний алиас из URL

    current_menu = Menu.objects.get(alias=current_alias)
    menus = Menu.objects.filter(parent_id=current_menu.id)

    bc_items = [('Деятельность', 'activity')]
    for slug in list(kwargs.values()):
        bc_items.append(
            (Menu.objects.get(alias=slug).title, slug)
        )

    context = {
        'data': 'normal',
        'bc_items': bc_items,
        'page': current_menu,
        'menus': menus,
    }
    # if request.GET.get('data') == 'component':
    #     context['data'] = 'component'
    #     return render(request, 'menus/menus.html', context)
    # else:
        # return render(request, 'menus/block_menus.html', context)
    return content_views.render_content(request, context)
