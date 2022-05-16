from django.shortcuts import render
from .models import Post, Feed
# from menus.models import Menu
# Create your views here.

def get_content(menu_id: int):
    ''' Возвращает контент, привязанный к меню'''
    has_content = False
    contents = {}

    # собираем посты
    contents['posts'] = Post.objects.filter(menu_id=menu_id)

    # собираем ленты
    contents['postfeeds'] = []
    feeds = Feed.objects.filter(menu__id=menu_id) 
    for feed in feeds:
        contents['postfeeds'].append({
            'feed': feed,
            'posts': feed.post_set.all()
        })
    
    # собираем информацию
    num_total = 0
    info = {'num':{}}
    for key, content  in contents.items():
        if len(content) > 0:
            has_content = True
            num_total += len(content)
            info['num'].update({key: len(content)})

    info['num']['total'] = num_total

    contents['info'] = info

    if has_content:
        return contents
    else:
        return False

def render_content(request, context):


    context['contents'] = get_content(context['page'].id)
    return render(request, 'content/content.html', context)