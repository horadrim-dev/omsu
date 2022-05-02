from django.shortcuts import render
from .models import Post
# Create your views here.

def get_content(menu_id: int):
    '''Проверяет есть ли контент, привязанный к меню'''
    has_content = False
    contents = {}

    contents['page'] = Post.objects.filter(menu_id=menu_id)
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
