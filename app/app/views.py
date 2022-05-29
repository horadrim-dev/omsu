from django.shortcuts import render
from menus import views as menus_views

def main(request, *args, **kwargs):
    return render(request, 'app/base.html', {})

def route(request, *args, **kwargs):
    return menus_views.menus(request, *args, **kwargs)

def sitemap(request, *args, **kwargs):
    return menus_views.sitemap(request, *args, **kwargs)
