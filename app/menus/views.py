from django.shortcuts import render
from . models import Menu, Page

def categories(request):
    context = {}
    
    context['category'] = None
    context['menus'] = Menu.objects.filter(parent_id__isnull=True)

    return render(request, 'menus/block_menus.html', context)

def subcategories(request, category=None):
    context = {}
    category = Menu.objects.filter(alias = category)[0]
    menus = Menu.objects.filter(parent_id = category.id)
    context = {
        'category' : category,
        'menus' : menus
    }
    return render(request, 'menus/block_menus.html', context)

def content(request, category=None, slug=None):
    context = {}
    category = Menu.objects.filter(alias = category)[0]
    subcategory = Menu.objects.filter(alias = slug)[0]
    submenus = Menu.objects.filter(parent_id = subcategory.id)

    contents = {}
    contents['page'] = Page.objects.filter(menu_id = subcategory.id)

    context = {
        'category' : category,
        'subcategory' : subcategory,
        'submenus' : submenus,
        'contents': contents
    }
    return render(request, 'menus/block_menus.html', context)

