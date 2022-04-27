from webbrowser import get
from django.shortcuts import render
from django.http import JsonResponse
from . models import Menu, Page


def categories(request):
    context = {}

    context['category'] = None
    context['menus'] = Menu.objects.filter(parent_id__isnull=True)
    bc_items = {
        'Деятельность': 'activity',
    }
    context['bc_items'] = bc_items
    return render(request, 'menus/block_menus.html', context)


# def subcategories(request, category=None):
#     context = {}
#     category = Menu.objects.filter(alias=category)[0]
#     menus = Menu.objects.filter(parent_id=category.id)
#     bc_items = {
#         'Деятельность': 'activity',
#         category.title: category.alias,
#     }
#     contents = {}
#     contents['page'] = Page.objects.filter(menu_id=category.id)

#     context = {
#         'bc_items': bc_items,
#         'category': category,
#         'menus': menus,
#         'contents': contents
#     }
#     return render(request, 'menus/block_menus.html', context)


# def content(request, category=None, slug=None):
#     context = {}

#     category = Menu.objects.filter(alias=category)[0]
#     subcategory = Menu.objects.filter(alias=slug)[0]
#     submenus = Menu.objects.filter(parent_id=subcategory.id)
#     bc_items = {
#         'Деятельность': 'activity',
#         category.title: category.alias,
#         subcategory.title: subcategory.alias
#     }

#     context = {
#         'bc_items': bc_items,
#         'category': category,
#         'subcategory': subcategory,
#         'submenus': submenus,
#         'contents': get_content(subcategory.id)
#     }
#     return render(request, 'menus/block_menus.html', context)


def get_content(menu_id: int):
    '''Проверяет есть ли контент, привязанный к меню'''
    has_content = False
    contents = {}

    contents['page'] = Page.objects.filter(menu_id=menu_id)
    # contents.append(list(Page.objects.filter(menu_id=menu_id)))

    num_contents = 0
    for content  in contents.values():
        if len(content) > 0:
            has_content = True
            num_contents += len(content)

    contents['config'] = {
        'num_contents': num_contents
    }

    if has_content:
        return contents
    else:
        return False


def menus(request, *args, **kwargs):
    current_alias = list(kwargs.values())[-1]  # берем последний алиас
    current_menu = Menu.objects.get(alias=current_alias)
    submenus = Menu.objects.filter(parent_id=current_menu.id)

    # if current_menu.parent_id:
    #     parent = Menu.objects.get(id=current_menu.parent_id)
    #     if parent.is_fixed:
    #         submenus = Menu.objects.filter(parent_id=current_menu.parent_id)

    category = current_menu
    contents = get_content(current_menu.id)

    bc_items = [('Деятельность', 'activity')]
    for slug in list(kwargs.values()):
        bc_items.append(
            (Menu.objects.get(alias=slug).title, slug)
        )

    if contents:
        menus = None
    else:
        menus = submenus
        submenus = None

    context = {
        'gt': request,
        'get': request.GET,
        'bc_items': bc_items,
        'category': category,
        'contents': contents,
        'menus': menus,
        'submenus': submenus
    }
    if request.GET.get('data') == 'component':
        return render(request, 'menus/html_menus.html', context)
    else:
        return render(request, 'menus/block_menus.html', context)
