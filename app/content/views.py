from django.shortcuts import render
from django.http import FileResponse, Http404
from django.conf import settings
from .models import Content, Post, Feed, Attachment
import os
# from menus.models import Menu
# Create your views here.

def get_content_if_exists(slug=None):
    '''возвращает объект контента по slug'''
    if slug:
        for content_type in Content.__subclasses__():
            # try:
                # return content_type.objects.get(alias=slug)
            obj = content_type.objects.filter(alias=slug)
            if len(obj) > 1:
                raise Http404('Получено несколько объектов с одинаковым alias')
            elif len(obj) == 1:
                return obj[0]
            # except:
            #     continue

        return False

def get_content(from_menu_id:int=None, from_slug:str=None):
    ''' Возвращает контент, привязанный к меню'''
    has_content = False
    contents = {}
    contents['posts'] = []
    contents['postfeeds'] = []

    if from_menu_id:
        posts = Post.objects.published().filter(menu_id=from_menu_id) # собираем посты
        feeds = Feed.objects.published().filter(menu__id=from_menu_id) # собираем ленты

    if from_slug: # контент на абстрактных страницах
        posts =  Post.objects.published().filter(alias=from_slug)
        feeds = None

    # post_ids = posts.values_list('id', flat=True)
    # attachments = Attachment.objects.filter(post__in=post_ids)#[x.attachment_set.all() for x in contents['posts']]
    for post in posts:
        contents['posts'].append({
            'post' : post,
            'attachments': post.attachment_set.all()
        })
    # contents['attachments'] = contents['posts'].attachment
    if feeds:
        for feed in feeds:
            contents['postfeeds'].append({
                'feed': feed,
                'posts': feed.post_set.published().all()
            })

    # собираем информацию
    num_total = 0
    info = {'count':{}}
    for key, content  in contents.items():
        if len(content) > 0:
            has_content = True
            num_total += len(content)
            info['count'].update({key: len(content)})

    info['count']['total'] = num_total

    contents['info'] = info

    if has_content:
        return contents
    else:
        return False

def render_content(request, context, unknown_slugs=None):
    if unknown_slugs:
        for slug in unknown_slugs:
            content = get_content_if_exists(slug)
            if content:
                context['bc_items'].append((content.title, slug))
            else:
                raise Http404('Контент не найден')
                
        context['page'] = content
        context['contents'] = get_content(from_slug=slug)
    else:
        context['contents'] = get_content(from_menu_id=context['page'].id)

    return render(request, 'content/content.html', context)


def download_attachment(request, uuid, *args, **kwargs):
    media_root = settings.MEDIA_ROOT
    try:
        attachment = Attachment.objects.get(uuid=uuid)
    except:
        raise Http404('Файл не найден.')

    if os.path.isfile(attachment.attached_file.path):
        attachment.hits += 1
        attachment.save()
        return FileResponse(
            open(attachment.attached_file.path, 'rb'),
            as_attachment=True,
            filename='{}.{}'.format(attachment.name[:100], attachment.extension)
        )
    else:
        raise Http404(
            'Файл "{}" в хранилище не найден.'.format(attachment.attached_file.path)
        )