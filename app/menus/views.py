from django.shortcuts import render
from . models import Menu, Page

def categories(request):
    context = {}
    
    context['category'] = None
    context['menus'] = Menu.objects.filter(parent_id__isnull=True)
    bc_items= {
        'Деятельность' : 'activity',
    }
    context['bc_items'] = bc_items
    return render(request, 'menus/block_menus.html', context)

def subcategories(request, category=None):
    context = {}
    category = Menu.objects.filter(alias = category)[0]
    menus = Menu.objects.filter(parent_id = category.id)
    bc_items= {
        'Деятельность' : 'activity',
        category.title : category.alias,
    }
    context = {
        'bc_items' : bc_items,
        'category' : category,
        'menus' : menus
    }
    return render(request, 'menus/block_menus.html', context)

def content(request, category=None, slug=None):
    context = {}

    category = Menu.objects.filter(alias = category)[0]
    subcategory = Menu.objects.filter(alias = slug)[0]
    submenus = Menu.objects.filter(parent_id = subcategory.id)
    bc_items = {
            'Деятельность' : 'activity',
            category.title : category.alias,
            subcategory.title : subcategory.alias
    }

    contents = {}
    contents['page'] = Page.objects.filter(menu_id = subcategory.id)

    context = {
        'bc_items' : bc_items,
        'category' : category,
        'subcategory' : subcategory,
        'submenus' : submenus,
        'contents': contents
    }
    return render(request, 'menus/block_menus.html', context)

