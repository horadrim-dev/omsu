from django.shortcuts import render
from django.views.generic import View, TemplateView, DetailView, ListView
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from toml import TomlDecodeError
from .forms import FeedFilterForm
from .models import ContentBase, Post, Feed, Attachment
from grid.models import Module
from menus.models import Menu
import datetime
import os
# from menus.models import Menu
# Create your views here.

# def get_content_if_exists(slug=None):
#     '''возвращает объект контента по slug'''
#     if slug:
#         for content_type in ContentBase.__subclasses__():
#             # try:
#                 # return content_type.objects.get(alias=slug)
#             obj = content_type.objects.published().filter(alias=slug)
#             if len(obj) > 1:
#                 raise Http404('Получено несколько объектов с одинаковым alias')
#             elif len(obj) == 1:
#                 return obj[0]
#             # except:
#             #     continue

#         return False

def get_related_content(menu:Menu=None, slug=None):
    
    for content_type in ContentBase.__subclasses__():

        if menu:
            obj = content_type.objects.published().filter(menu=menu)
        elif slug:
            obj = content_type.objects.published().filter(alias=slug)

        if len(obj) > 1:
            raise Http404('Получено несколько объектов')
        elif len(obj) == 1:
            return obj[0]

    return None


def get_extracontent(menu:Menu=None, module:Module=None):
    ''' Возвращает экстраконтент, привязанный к меню или модулям'''
    # todo: Переделать в get_extracontent 
    if module:
        return module.modulecontent_set.all()

    if menu:
        contents = {}
        # contents['content'] = [menu]

        for content in menu.extracontent_set.all():
            if content.position not in contents:
                contents[content.position] = [content]
            else:
                contents[content.position].append(content)

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
class TestView(DetailView):
    model = Feed
    template_name = 'content/feed_detail.html'
    # slug_field = 'alias'
    # slug_url_kwarg = 'slug'
    # def get_object(self):
    #         object = super().get_object()
    #         return object

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # assert False, context
        return context

class FeedDetailView(DetailView): 
    template_name = 'content/layout_feed.html'
    object = None
    model = Feed
    post_filter = {}
    post_filter_form = FeedFilterForm
    open_filter_form = False
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # используем форму для валидации get параметров
        form = FeedFilterForm(request.GET)
        if not form.is_valid():
            # assert False,(form.errors.keys())
            messages.warning(
                request, 
                'Некорректные параметры запроса: "{}"'
                .format(', '.join(form.errors.keys()))
            )
        self.cleaned_GET = form.cleaned_data

    def dispatch(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or request.GET.get('ajax'):
            return self.ajax_get(request, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context.update({
            'layout': 'normal',
            'uid' : 'content',
            'paginator':self.object.get_page(
                page=self.cleaned_GET.get('page', 1),
                post_filter=self.post_filter, 
                posts_per_page=self.object.feed_count_items
                ),
            'post_filter_form' : self.post_filter_form,
            'open_filter_form' : self.open_filter_form
        })

        return context

    def render_to_string(self, context):
        # assert False, context
        return render_to_string(
                self.template_name, context, request=self.request
            )

    def get(self, request, *args, **kwargs):
        # object получать не надо - он уже передан в атрибут
        # получаем контекст
        context = self.get_context_data(object = self.object)
        return self.render_to_string(context)
    
    def ajax_get(self, request, *args, **kwargs):
        # return super().get(request, *args, **kwargs)
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        context['requested_with_ajax'] = True
        return HttpResponse(self.render_to_string(context))

    def post(self, request):
        self.post_filter_form = self.post_filter_form(request.POST)

        if self.post_filter_form.is_valid():
            # передаем в фильтр чистые данные
            self.post_filter = self.post_filter_form.cleaned_data

            messages.success(request, 'Данные отфильтрованы')
            # открываем форму фильтра
            self.open_filter_form = True 
        else:
            # очищаем форму
            self.post_filter_form = FeedFilterForm()

        return self.render_to_string()

    # def ajax(self, request, slug):
    #     if feed:

    # def render_to_response(self, context, **response_kwargs):
    #     """ Allow AJAX requests to be handled more gracefully """
    #     if self.request.is_ajax():
    #         return JSONResponse('Success',safe=False, **response_kwargs)
    #     else:
    #         return super(TemplateView,self).render_to_response(context, **response_kwargs)

class PostListView(ListView):
    model = Post
    feed = None
    context_object_name = 'hui_list'
    def get_context_data(self, **kwargs):
        assert False, super().get_context_data(**kwargs)


class PostDetailView(DetailView):
    template_name = 'content/layout_post.html'
    object = None
    model = Post

    def render_to_string(self, context):
        return render_to_string(self.template_name, context, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attachments'] = self.object.get_attachments()
        return context

    def get(self, request):
        # object получать не надо - он уже передан в атрибут
        context = self.get_context_data()
        return self.render_to_string(context)

    # def post(self, request):
    #     return self.render_to_string()


def render_content(request, context, unknown_slugs=None):

    page_content = get_related_content(menu=context['page'])
    page_title = context['page'].title

    if unknown_slugs:
        # Если есть slug-и "не меню" то проверяем их и передаем на обработку
        # разным функциям (зависит от контент-типа текущего меню)
        unknown_objects = []
        for slug in unknown_slugs:
            obj = get_related_content(slug=slug)
            ### Здесь должна быть проверка на родство [slugs между собой]
            ### и [первого slug с последним меню]
            if obj:
                unknown_objects.append(obj)
                context['bc_items'].append((obj.title, slug))
            else:
                raise Http404('Контент не найден')
                
        # context['page'] = content
        # context['contents'] = get_content(slug=slug)
        if page_content.__class__.__name__ == 'Feed':
            # ПРОДУМАТЬ НАСЛЕДОВАНИИЕ ЛЕНТ
            if len(unknown_objects) == 1 :

                if (unknown_objects[0].__class__.__name__ == 'Post'):

                    post = unknown_objects[0]

                    if post.feed != page_content:
                        raise Http404('Проверка на родство ленты и поста не пройдена')

                    page_title = post.title
                    # CONTENT_HTML = post.render_html()
                    CONTENT_HTML = PostDetailView.as_view(object=post)(request)
                else:
                    raise Http404('Для меню-ленты unknown_slug!=Post не предусмотрен.')
            else:
                raise Http404('Получено {} unknown_slugs, не предусмотрено'.format(len(unknown_objects)))

        elif page_content.__class__.__name__ == 'Post':
            raise Http404('Не продумано.(unknown_slug после меню-поста)')
        else:
            raise Http404('Не продумано.(unknown_slug = {})'.format())

    else:
        if page_content.__class__.__name__ == 'Post':
            CONTENT_HTML = PostDetailView.as_view(object=page_content)(request)
        elif page_content.__class__.__name__ == 'Feed':
            CONTENT_HTML = FeedDetailView.as_view(object=page_content)(request)
            # CONTENT_HTML = PostListView.as_view()(request)
        else:
            CONTENT_HTML = page_content.render_html(request) if page_content else None


    context['page_title'] = page_title  
    context['CONTENT_HTML'] = CONTENT_HTML
    context['contents'] = get_extracontent(menu=context['page'])

    for section in context['sections']:
        for column in section['columns']:
            for module in column['modules']:
                module['contents'] = get_extracontent(module=module['obj'])


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
    context['feed_style'] = request.GET.get('layout')

    return render(request, 'content/layout_feed.html', context)

# def ajax_post(request, *args, **kwargs):
#     # if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
#     #     raise Http404()
#     if not request.GET.get('post'):
#         return Http404()

#     context = {}
#     try:
#         post = Post.objects.published().get(alias=request.GET.get('post'))
#     except Exception:
#         raise Http404('Пост не найден')
    
#     context['post'] = post
#     context['attachments'] = post.get_attachments()

#     return render(request, 'content/layout_post.html', context)