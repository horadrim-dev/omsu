from django.shortcuts import render
from django.views.generic import View, TemplateView, DetailView, ListView
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from toml import TomlDecodeError
from .forms import FeedFilterForm, FeedValidationForm
from .models import ContentBase, Post, Feed, Attachment
from grid.models import Module
from menus.models import Menu
import datetime
import os
# from menus.models import Menu
# Create your views here.

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

    return contents


class FeedDetailView(DetailView): 

    template_name = 'content/layout_feed.html'
    object = None
    model = Feed

    post_filter = {}
    post_filter_form = FeedFilterForm
    show_filter = False
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        
        # валидируем get параметры формы - фильтра
        form = FeedFilterForm(request.GET)
        if not form.is_valid():
            messages.warning(
                request, 
                'Некорректные параметры запроса: "{}"'
                .format(', '.join(form.errors.keys()))
            )
        self.post_filter = form.cleaned_data
        self.post_filter_form = form
        for value in self.post_filter.values():
            if value:
                # assert False, self.post_filter
                messages.success(request, 'Данные отфильтрованы')
                self.show_filter = True
                break

        # используем форму для валидации остальных get параметров
        form = FeedValidationForm(request.GET)
        if not form.is_valid():
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
    
    def post_filter_params_as_row(self):
        '''Возвращает строку параметров для использования в форме в url'''
        params_list = []
        for key, value in self.post_filter.items():
            # проверка на дату
            if isinstance(value, datetime.date):
                # переформатируем дату в требуемый формой формат
                value = value.strftime("%d.%m.%Y")
            if not value:
                value = ''
            params_list.append( str(key) + '=' + str(value) )

        return '&' . join(params_list)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            'layout': 'normal',
            'uid' : 'content',
            'feed_style' : self.object.feed_style,
            'columns' : self.object.feed_num_columns,
            'paginator':self.object.get_page(
                page=self.cleaned_GET.get('page', 1),
                post_filter=self.post_filter, 
                posts_per_page=self.object.feed_count_items
                ),
            'post_filter_form' : self.post_filter_form,
            'show_filter' : self.show_filter,
            'filter_params_row' : self.post_filter_params_as_row()
        })

        return context

    def render_to_string(self, context):
        return render_to_string(
                self.template_name, context, request=self.request
            )

    def get(self, request, *args, **kwargs):
        # object получать не надо - он уже должен быть передан в атрибут FeedView
        # Проверка что объект feed задан - если нет - 
        # значит ктото пытается открыть форму для ajax подгрузки страниц "/content/ajax/feed/*/?params"
        if not self.object:
            raise Http404()
        # получаем контекст
        context = self.get_context_data(object = self.object)
        return self.render_to_string(context)
    
    def ajax_get(self, request, *args, **kwargs):
        # return super().get(request, *args, **kwargs)
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        context['requested_with_ajax'] = True
        return HttpResponse(self.render_to_string(context))

    # def post(self, request):
    #     self.post_filter_form = self.post_filter_form(request.POST)

    #     if self.post_filter_form.is_valid():
    #         # передаем в фильтр чистые данные
    #         self.post_filter = self.post_filter_form.cleaned_data

    #         messages.success(request, 'Данные отфильтрованы')
    #         # открываем форму фильтра
    #         self.show_filter = True 
    #     else:
    #         # очищаем форму
    #         self.post_filter_form = FeedFilterForm()

    #     return self.render_to_string()


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
            # CONTENT_HTML = TestVueView.as_view(object=page_content)(request)
        else:
            CONTENT_HTML = 'XYU TEBE A NE CONTENT'
            # assert False, page_content.__class__.__name__
            # raise NotImplementedError('НУЖНА НОВАЯ ВЬЮХА!!!')


    context['page_title'] = page_title  
    context['CONTENT_HTML'] = CONTENT_HTML
    context['contents'] = get_extracontent(menu=context['page'])

    for section in context['sections']:
        for column in section['columns']:
            for module in column['modules']:
                module['contents'] = get_extracontent(module=module['obj'])


    return render(request, 'content/content.html', context)

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