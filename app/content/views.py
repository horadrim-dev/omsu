from django.shortcuts import render
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator
from .models import ContentBase, Post, Feed, Attachment
from grid.models import Module
from menus.models import Menu
import os
# from menus.models import Menu
# Create your views here.

def get_content_if_exists(slug=None):
    '''возвращает объект контента по slug'''
    if slug:
        for content_type in ContentBase.__subclasses__():
            # try:
                # return content_type.objects.get(alias=slug)
            obj = content_type.objects.published().filter(alias=slug)
            if len(obj) > 1:
                raise Http404('Получено несколько объектов с одинаковым alias')
            elif len(obj) == 1:
                return obj[0]
            # except:
            #     continue

        return False

def get_content(menu:Menu=None, slug:str=None, module:Module=None):
    ''' Возвращает контент, привязанный к меню'''
    if module:
        return module.modulecontent_set.all()

    if menu:
        contents = {}
        for content in menu.content_set.all():
            if content.position not in contents:
                contents[content.position] = [content]
            else:
                contents[content.position].append(content)

    if slug:
        Http404('UNKNOWN SLUG - hz')
        

    # has_content = False
    # contents = {}
    # contents['posts'] = []
    # contents['postfeeds'] = []
    # contents['menus'] = []
    # if from_menu_id:
    #     posts = Post.objects.published().filter(menu_id=from_menu_id) # собираем посты
    #     feeds = Feed.objects.published().filter(menu__id=from_menu_id) # собираем ленты
    #     menus = None
    # elif from_slug: # контент на абстрактных страницах
    #     posts =  Post.objects.published().filter(alias=from_slug)
    #     feeds = None
    #     menus = None
    # elif module:
        # posts = Post.objects.published().filter(id=module.post_content_id)
        # feeds = Feed.objects.published().filter(id=module.feed_content_id)
        # # menus = Menu.objects.published().filter(id=module.menu_content_id)
        # posts = []
        # feeds = None
        # menus = []
        # assert False, (module, Menu.objects.published)
        # assert False, (module, module.modulecontent_set.all())
    # post_ids = posts.values_list('id', flat=True)
    # attachments = Attachment.objects.filter(post__in=post_ids)#[x.attachment_set.all() for x in contents['posts']]
    # for post in posts:
    #     contents['posts'].append({
    #         'post' : post,
    #         'attachments': post.get_attachments()
    #     })

    # if menus:
    #     for menu in menus:
    #         contents['menus'].append({
    #             'parent': menu,
    #             'subitems': menu.get_subitems()
    #         })

    # if feeds:
    #     for feed in feeds:
    #         contents['postfeeds'].append({
    #             'feed': feed,
    #             'posts': feed.get_page(page=1),
    #         })

    # собираем информацию
    # num_total = 0
    # info = {'count':{}}
    # for key, content  in contents.items():
    #     if len(content) > 0:
    #         has_content = True
    #         num_total += len(content)
    #         info['count'].update({key: len(content)})

    # info['count']['total'] = num_total

    # contents['info'] = info

    return contents
    # if has_content:
    #     return contents
    # else:
    #     return False

def render_content(request, context, unknown_slugs=None):
    if unknown_slugs:
        for slug in unknown_slugs:
            content = get_content_if_exists(slug)
            if content:
                context['bc_items'].append((content.title, slug))
            else:
                raise Http404('Контент не найден')
                
        context['page'] = content
        context['contents'] = get_content(slug=slug)
    else:
        context['contents'] = get_content(menu=context['page'])

    for section in context['sections']:
        for column in section['columns']:
            for module in column['modules']:
                module['contents'] = get_content(module=module['obj'])


    return render(request, 'content/content.html', context)

# def render_module

def download_attachment(request, uuid, *args, **kwargs):
    # media_root = settings.MEDIA_ROOT
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

def ajax_feed_page(request, slug, *args, **kwargs):
    # if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     raise Http404()

    context = {}
    try:
        feed = Feed.objects.published().get(alias=slug)
    except Exception:
        raise Http404('Лента не найдена')
    
    context['feed'] = feed

    if request.GET.get('items_per_page'):
        context['count_items'] = int(request.GET.get('items_per_page'))

    if request.GET.get('page'):
        if request.GET.get('items_per_page') :
            context['posts'] = feed.get_page(
                page=request.GET.get('page'), posts_per_page=context['count_items']
            )
        else:
            context['posts'] = feed.get_page(page=request.GET.get('page'))
    else:
        context['posts'] = feed.get_page()

    context['uid'] = request.GET.get('uid') # для использования в качестве уникального id в шаблоне
    context['layout'] = request.GET.get('layout')

    return render(request, 'content/post_list.html', context)

def ajax_post(request, *args, **kwargs):
    # if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     raise Http404()
    if not request.GET.get('post'):
        return Http404()

    context = {}
    try:
        post = Post.objects.published().get(alias=request.GET.get('post'))
    except Exception:
        raise Http404('Пост не найден')
    
    context['post'] = post
    context['attachments'] = post.get_attachments()

    return render(request, 'content/post.html', context)