# from webbrowser import get
# from asyncio.windows_events import NULL
from django.shortcuts import render
# from django.http import JsonResponse
from . models import Menu
from content import views as content_views

def get_menu_if_exists(slug=None):
    if slug:
        try:
            obj = Menu.objects.get(alias=slug)
        except:
            return False

        return obj


def menus(request, section=None, *args, **kwargs):

    unknown_slugs = []
    bc_items = [(section.title, section.alias)]
    current_menu = section 

    # перебираем кварги пока не наткнемся на несуществующий в меню
    # все кварги-меню заносим в breadcrumbs
    # все неизвестные кварги передаем дальше в контент
    if len(kwargs) > 0:
        urlpath = list(kwargs.values())

        for i, slug in enumerate(urlpath):
            obj = get_menu_if_exists(slug)
            if obj:
                current_menu = obj
                bc_items.append((current_menu.title, slug))
            else:
                unknown_slugs += urlpath[i:]
                break


    menus = Menu.objects.filter(parent_id=current_menu.id)

    context = {
        'section':section,
        # 'data': 'normal',
        'bc_items': bc_items,
        'page': current_menu,
        'menus': menus,
    }
    # if request.GET.get('data') == 'component':
    #     context['data'] = 'component'
    #     return render(request, 'menus/menus.html', context)
    # else:
        # return render(request, 'menus/block_menus.html', context)
    return content_views.render_content(request, context, unknown_slugs)

def sitemap(request, *args, **kwargs):
    context = {}
    context['menu_tree'] = Menu.get_subitems(parent=None, maxlevel=None)
    context['bc_items'] = [('Карта сайта', 'sitemap')]
    return render(request, 'menus/sitemap.html', context)