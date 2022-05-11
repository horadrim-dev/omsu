from django.shortcuts import render
from .models import Post, Feed
# from menus.models import Menu
# Create your views here.

def get_content(menu_id: int):
    ''' Возвращает контент, привязанный к меню'''
    has_content = False
    contents = {}

    contents['posts'] = Post.objects.filter(menu_id=menu_id)
    contents['feeds'] = Feed.objects.filter(menu__id=menu_id)
    # contents.append(list(Page.objects.filter(menu_id=menu_id)))

    num_contents = 0
    for content  in contents.values():
        if len(content) > 0:
            has_content = True
            num_contents += len(content)

    contents['info'] = {
        'num_contents': num_contents
    }

    if has_content:
        return contents
    else:
        return False

def render_content(request, context):


    context['contents'] = get_content(context['page'].id)
    return render(request, 'content/content.html', context)