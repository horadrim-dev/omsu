# from ast import arg
# from re import A
# from tabnanny import verbose
import re
from tkinter import CASCADE
from urllib.request import AbstractDigestAuthHandler
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django.forms import ValidationError
from django.http import Http404
from django.template.loader import render_to_string
# from django.utils import timezone
from django.conf import settings
# from menus.models import Menu
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from app.utils import slugify_rus, remove_empty_dirs
from app.models import OrderedModel
from django.core.paginator import Paginator
from django.apps import apps
from . import app_settings as content_settings
import datetime
import os
import uuid
from taggit_selectize.managers import TaggableManager
# Create your models here.


def attachment_upload_location(instance, filename=None):
    '''Формирует относительный путь для сохранения вложений'''
    # _ , extension = os.path.splitext(filename)
    filename = '.'.join([slugify_rus(instance.name), instance.extension])
    path = 'attachments'
    # если у поста есть привязка к меню, сохраняем с аналогичной меню директорией
    if instance.post.menu:
        return ''.join([path, instance.post.menu.url, filename])

    # если привязки к меню нет, то сохраняем в директорию feeds/feed_alias
    if instance.post.feed:
        return '/'.join([
            path,
            'feeds', 
            instance.post.feed.alias, 
            instance.published_at.strftime('%Y/%m/%d'), 
            filename
        ])

    return False

class ContentManager(models.Manager):

    def published(self):
        return self.filter(published=True, published_at__lte=datetime.date.today())

class ContentBase(models.Model):

    menu = models.ForeignKey(
        'menus.Menu', on_delete=models.SET_NULL, verbose_name="Привязка к меню", blank=True, null=True)
    title = models.CharField(
        default="", max_length=1000, verbose_name="Заголовок")
    alias = models.SlugField(default="", blank=True, unique=True,
                             max_length=1000, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    published = models.BooleanField(default=True, verbose_name='Опубликовано')
    published_at = models.DateField(default=datetime.date.today, 
                                    verbose_name="Дата публикации")
    # created_at = models.DateTimeField(default=timezone.now,
    #                                 verbose_name="Дата создания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")
    hits = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")

    objects = ContentManager()

    def save(self, lock_recursion=False, *args, **kwargs):
        # только при создании объекта, id еще не существует
        if not self.id or not self.alias:
            # заполняем алиас
            self.alias = slugify_rus(self.title)

        super(ContentBase, self).save(*args, **kwargs)
    
    def clean(self):
        # Проверка один меню - один контент
        if self.menu:
            objs = []
            for content_type in ContentBase.__subclasses__():
                qs = content_type.objects.filter(menu=self.menu)

                if self.id:
                    qs = qs.exclude(id=self.id)

                objs = objs + list(qs)
                
            if len(objs) > 0:
                raise ValidationError(
                    {'menu' : ('К меню "{}" уже привязан контент "{}". \
                            Больше одной привязки не допускается. \
                            Воспользуйтесь Дополнительным контентом (Меню->Дополнительный контент)'.format(
                                self.menu, [obj.title for obj in objs]
                            )
                        )
                    }
                )
    
    def render_html(self):
        assert False, 'Добавь контенту метод render_html, идиот'

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['-published_at']


class FeedLayout(models.Model):

    FEED_STYLE_CHOICES = [
        ('feed', 'Список постов'),
        ('compact_feed', 'Список постов (только заголовки)'),
        ('blocks', 'Посты в виде блоков (без изображений)'),
        ('blocks_with_images_left', 'Посты в виде блоков (изображения слева)'),
        ('blocks_with_images_top', 'Посты в виде блоков (изображения сверху)'),
        ('slider', 'Слайдер постов'),
    ]
    feed_style = models.CharField(max_length=64, choices=FEED_STYLE_CHOICES, default=FEED_STYLE_CHOICES[0][0],
        verbose_name="Макет ленты постов")
    FEED_COLUMN_CHOICES = [
        (1, '1 колонка'),
        (2, '2 колонки'),
        (3, '3 колонки'),
        (4, '4 колонки'),
    ]
    feed_num_columns = models.PositiveSmallIntegerField(choices=FEED_COLUMN_CHOICES, default=FEED_COLUMN_CHOICES[1][0],
        verbose_name="Количество колонок")
    feed_count_items = models.PositiveSmallIntegerField(default=6, verbose_name="Количество выводимых постов")
    # feed_readmore = models.BooleanField(default=True, verbose_name="Отображать кнопку \"Читать больше\"")
    FEED_SORT_DIRECTION_CHOICES = [
        ('horizontal', 'Построчно'),
        ('vertical', 'По колонкам'),
    ]
    feed_sort_direction = models.CharField(max_length=16, choices=FEED_SORT_DIRECTION_CHOICES, default=FEED_SORT_DIRECTION_CHOICES[0][0],
        verbose_name="Направление сортировки")

    class Meta:
        abstract = True


class Feed(ContentBase, FeedLayout):

    menu = models.ForeignKey('menus.Menu', on_delete=models.SET_NULL, verbose_name="Привязка к меню", null=True)
    parent = models.ForeignKey(
        'content.Feed', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родительская лента")
    show_childs = models.BooleanField(default=True, verbose_name="Отображать посты из дочерних лент")
    description = RichTextUploadingField(blank=True, null=True)

    def get_url(self):
        if self.menu:
            return self.menu.url

    def get_child_feeds(self):
        return Feed.objects.published().filter(parent=self)

    def get_posts(self, post_filter):
        # запрашиваем посты в зависимости от опции показа дочерних лент
        if self.show_childs:
            qs = Post.objects.published().filter(
                models.Q(feed__in=self.get_child_feeds())
                |
                models.Q(feed=self)
            )
        else:
            qs = self.post_set.published()

        # если фильтр задан - применяем
        if post_filter:
            if post_filter.get('date_start', None):
                qs = qs.filter(published_at__gte=post_filter['date_start'])
            if post_filter.get('date_end', None):
                qs = qs.filter(published_at__lte=post_filter['date_end'])
            if post_filter.get('q', None):
                qs = qs.filter(models.Q(title__icontains=post_filter['q'])) #| models.Q(text__icontains=q))

        return qs
    
    def get_page(self, page=None, post_filter=None, posts_per_page=content_settings.NUM_POSTS_ON_FEED_PAGE):
        paginator = Paginator(
            # self.post_set.published().all(), posts_per_page
            self.get_posts(post_filter=post_filter), posts_per_page
        )
        return paginator.get_page(page)
    
    # def render_html(self, request):
    #     from .forms import FeedFilterForm # circular import
        
    #     return render_to_string(
    #             'content/layout_feed.html', 
    #             {
    #                 'feed':self, 
    #                 'posts':self.get_page(request, posts_per_page=self.feed_count_items),
    #                 'feed_style':self.feed_style,
    #                 'columns': self.feed_num_columns,
    #                 'count_items': self.feed_count_items,
    #                 'sort_direction': self.feed_sort_direction,
    #                 'readmore': self.feed_readmore,
    #                 'feed_filter_form' : FeedFilterForm
    #             })

    class Meta:
        verbose_name = "Лента постов"
        verbose_name_plural = "Ленты постов"


class PostLayout(models.Model):
    class Meta:
        abstract = True


class Post(ContentBase, PostLayout):

    feed = models.ForeignKey(
        Feed, on_delete=models.SET_NULL, verbose_name="Лента постов", blank=True, null=True)
    # feed = models.ManyToManyField(Feed, blank=True, verbose_name="Лента")
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/", verbose_name="Изображение поста",
        blank=True, null=True)
    IMAGE_POSITION_CHOICES = [
        ('left', 'Слева'),
        ('stretch', 'Растянуть'),
        ('right', 'Справа'),
        ('hide', 'Скрыть'),
    ]
    image_position = models.CharField(max_length=64, choices=IMAGE_POSITION_CHOICES, default=IMAGE_POSITION_CHOICES[0][0],
        verbose_name="Расположение изображения")
    tags = TaggableManager()
    intro_text = RichTextField(blank=True)
    text = RichTextUploadingField()

    def save(self, *args, **kwargs):

        intro = self.text.split('</p>')
        if len(intro) >= 2:
            self.intro_text = intro[0] + '</p>' + intro[1] + '</p>'
        else:
            self.intro_text = '<p></p>'

        super(Post, self).save(*args, **kwargs)
    
    def get_url(self):
        if self.feed and self.feed.menu:
            return self.feed.menu.url + self.alias
    def count_attachments(self):
        '''Возвращает количество связанных attachments'''
        return self.attachment_set.all().count()

    def get_attachments(self, *args, **kwargs):
        '''Возвращает все связанные объекты attachments'''
        return self.attachment_set.all()

    def relocate_attachments(self, *args, **kwargs):
        '''Обновляет расположение вложений, связанных с постом'''
        attachments = self.attachment_set.all()

        for attachment in attachments:
            attachment.update_location()
        
        return len(attachments)

    # def render_html(self, request):
    #     # для поста пока макет только один, поэтому все просто:
    #     return render_to_string(
    #             'content/layout_post.html', 
    #             {'post':self, 'attachments':self.get_attachments()}
    #             )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-published_at']


@receiver(models.signals.post_delete, sender=Post)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Удаляет фото при удалении поста
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)



class Attachment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    name = models.CharField(default="", max_length=1000,
                            verbose_name="Название")
    extension = models.CharField(default="", max_length=16, blank=True, 
                                verbose_name="Расширение файла")
    attached_file = models.FileField(upload_to=attachment_upload_location, 
                                    verbose_name='Вложение')
    published_at = models.DateField(default=datetime.date.today, 
                                    verbose_name="Дата публикации")
    hits = models.PositiveIntegerField(default=0, verbose_name="Кол-во загрузок")

    def __str__(self):
        return self.name
    
    def url(self):
        '''Формирует url для скачивания'''
        return reverse('attachment_download', kwargs={'uuid': self.uuid})

    def update_location(self):
        '''Проверяет правильно ли расположен файл, если нет -
        перемещает в нужную директорию'''
        filename = attachment_upload_location(self,'')

        if self.attached_file.name != filename:
            old_filepath = self.attached_file.path # абсолютный путь к старому файлу
            old_dirpath = os.path.split(old_filepath)[0] # абсолютный путь к старой папке
            filedir, short_filename = os.path.split(filename) # относительный путь к новой папке и новое имя файла
            dirpath = '/'.join([settings.MEDIA_ROOT, filedir]) # абсолютный путь к новой папке
            filepath = '/'.join([dirpath, short_filename]) # абсолютный путь к новому файлу
            if not os.path.exists(dirpath): # проверяем что каталог существует
                os.makedirs(dirpath)
            os.rename(self.attached_file.path, filepath) # переносим файл
            # удаляем старую директорию (если файлов больше нет)
            remove_empty_dirs(old_dirpath) # app/utils.py
            self.attached_file = filename # присваиваем полю новый путь
            self.save()

            return self.attached_file
        else:
            return False

    def save(self,  *args, **kwargs):
        # считываем расширение файла
        self.extension = self.attached_file.path.split('.')[-1].lower()

        super(Attachment, self).save(*args, **kwargs)

        self.update_location()


@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Удаляет файл при удалении объекта вложения
    """
    if instance.attached_file:
        if os.path.isfile(instance.attached_file.path):
            os.remove(instance.attached_file.path)
            
# @receiver(models.signals.post_save, sender=Post)
# def relocate_attachments(sender, instance, **kwargs):


class MenuLayout(models.Model):

    MENU_STYLE_CHOICES = [
        ('horizontal_blocks', 'Горизонтальное меню (блоки)'),
        ('vertical_with_submenus', 'Вертикальное меню (с дочерними меню)'),
        ('vertical_without_submenus', 'Вертикальное меню (без дочерних меню)'),
    ]
    menu_style = models.CharField(max_length=64, choices=MENU_STYLE_CHOICES, default=MENU_STYLE_CHOICES[0][0],
        verbose_name="Макет меню")

    class Meta:
        abstract = True


class ContentLayoutBase(models.Model):

    class Meta:
        abstract = True
        # verbose_name = "Контент"
        # verbose_name_plural = "Контент"
        # ordering = ['order']


class ContentLayout(ContentLayoutBase, FeedLayout, MenuLayout, PostLayout):

    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    CONTENT_TYPE_CHOICES = [
        ('', '---'),
        ('post', 'Пост'),
        ('feed', 'Лента постов'),
        ('menu', 'Меню'),
    ]
    content_type = models.CharField(max_length=64, choices=CONTENT_TYPE_CHOICES , default=CONTENT_TYPE_CHOICES[0][0],
        verbose_name="Тип контента")

    # называть поля с контентом нужно с содержанием названия из CONTENT_TYPE_CHOICES (для работы JS) (пример: post,post_style,hzpost)

    content_post = models.ForeignKey(
        Post, on_delete=models.SET_NULL, verbose_name="Пост", blank=True, null=True)

    content_feed = models.ForeignKey(
        Feed, on_delete=models.SET_NULL, verbose_name="Лента постов", blank=True, null=True)

    content_menu = models.ForeignKey(
        'menus.Menu', on_delete=models.SET_NULL, related_name="+", verbose_name="Меню", blank=True, null=True)

    class Meta:
        # abstract = True
        verbose_name = "Макет контента"
        # verbose_name_plural = "Контент"
        # ordering = ['order']

    def get_alias(self):
        if self.content_type == 'post':
            return self.content_post.alias
        if self.content_type == 'feed':
            return self.content_feed.alias
        if self.content_type == 'menu':
            return self.content_menu.alias
        return super().get_alias()

    def get_title(self):
        if self.content_type == 'post':
            return self.content_post.title
        if self.content_type == 'feed':
            return self.content_feed.title
        if self.content_type == 'menu':
            return self.content_menu.title
        return super().get_title()

    def __str__(self):
        if self.content_type == 'feed':
            return 'Лента постов: ({})'.format(self.content_feed.title) if self.content_feed else 'Не выбран'
        if self.content_type == 'post':
            return 'Пост: ({})'.format(self.content_post.title) if self.content_post else 'Не выбран'
        if self.content_type == 'menu':
            return 'Меню: ({})'.format(self.content_menu.title) if self.content_menu else 'Не выбран'
        return super().__str__()

    def get_feed_page(self):
        if self.content_type == 'feed' and self.content_feed:
            return self.content_feed.get_page(posts_per_page=self.feed_count_items)


class ExtraContent(OrderedModel, ContentLayout):
    
    # contentlayout_ptr = models.OneToOneField(to=ContentLayout, parent_link=True, on_delete=models.CASCADE, related_name='extracontent')

    tied_to_menu = models.ForeignKey('menus.Menu', on_delete=models.CASCADE, verbose_name="Привязка к меню")

    show_title = models.BooleanField(default=False, verbose_name="Отображать заголовок")

    POSITION_CHOICES = [
        # ('content', 'Контент'),
        ('right', 'Справа'),
        ('left', 'Слева'),
        ('bottom', 'Внизу'),
        ('top', 'Сверху'),
        ('stacked', 'Под постом (В виде ленты)'),
    ]
    position = models.CharField(max_length=64, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0],
        verbose_name="Расположение")

    class Meta:
        verbose_name = "дополнительный контент"
        verbose_name_plural = "дополнительный контент"
        ordering = ['order']

    def save(self, lock_recursion=False, *args, **kwargs):

        super(ExtraContent, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(ExtraContent.objects.filter(tied_to_menu=self.tied_to_menu, position=self.position).exclude(id=self.id))
            )

