# from asyncore import loop
# from tkinter import CASCADE
# from unittest.util import _MAX_LENGTH
from django.db import models, transaction
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ValidationError
# from ckeditor.fields import RichTextField
from app.utils import slugify_rus
from app.models import OrderedModel
from content.models import ContentLayout, Feed
# import content.models as c_models
# from django.db.models import F

# Create your models here.

class MenuManager(models.Manager):

    def published(self):
        return self.filter(published=True)

class Menu(ContentLayout, OrderedModel):
    # content_layout = models.OneToOneField(to=ContentLayout, default='', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Название")
    alias = models.SlugField(blank=True, unique=True,
                             max_length=100, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    parent = models.ForeignKey(
        'menus.Menu', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родитель")
    # order = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    list_order = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    level = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    url = models.CharField(max_length=1000, default='', blank=True, null=True)

    published = models.BooleanField(default=True, verbose_name="Опубликовано")
    megamenu = models.BooleanField(default=False, verbose_name="Мегаменю",
                                   help_text="Если отмечено, меню будет выпадать шириной во весь экран")
    icon = models.CharField(max_length=32, default="", blank=True, verbose_name="Иконка", help_text="Необязательно. Названия брать <a href='https://icons.getbootstrap.com/' target='_blank'>отсюда.</a>")
    short_description = models.CharField(max_length=100, blank=True,
        verbose_name="Краткое описание", help_text="Краткое описание содержимого меню")
    description = RichTextUploadingField(verbose_name="Описание", blank=True)
    debug_info = models.TextField(default="", blank=True, null=True)

    objects = MenuManager()

    def clean(self):

        if self.content_type == 'menu':
            # Проверка на выбор меню
            if not self.content_menu:
                raise ValidationError({'content_menu' : ('Необходимо выбрать меню')})
        
        if self.content_type == 'post':
            # Проверка на выбор поста
            if not self.content_post:
                raise ValidationError({'content_post' : ('Необходимо выбрать пост')})

        if self.content_type == 'feed':
            # Проверка на выбор ленты
            if not self.content_feed:
                raise ValidationError({'content_feed' : ('Необходимо выбрать ленту')})
            # Проверка "Одна лента - один меню"
            qs = Menu.objects.filter(
                content_type='feed', 
                content_feed=self.content_feed
                ).exclude(id=self.id)
            if len(qs) > 0:
                msg = 'Лента "{}" уже привязана к меню "{}". \
                    Если вы хотите отобразить эту ленту на этой странице\
                     - воспользуйтесь разделом "Дополнительный контент"'\
                    .format(self.content_feed, qs[0].title)
                raise ValidationError({
                    'content_feed' : (msg)
                    })

    def save(self, lock_recursion=False, *args, **kwargs):
        # только при создании объекта, id еще не существует
        if not self.id:
            if not self.alias:
                # заполняем алиас
                self.alias = slugify_rus(self.title)

        # заполняем поле уровня вложенности меню
        if self.parent_id:
            self.level = Menu.objects.get(id=self.parent_id).level + 1
        else:
            self.level = 1
        
        self.url = self.get_url_path(self.alias)

        super(Menu, self).save(*args, **kwargs)

        # обновляем порядок
        if not lock_recursion:
            self.update_order(
                list_of_objects = list(Menu.objects.filter(parent=self.parent).exclude(id=self.id))
            )
            self.update_list_order()
            # обновляем URL в дочерних объектах
            self.update_urls()
        # обновляем дочерние объекты
        self.update_subitems_level()

    def update_urls(self):
        '''Обновляет URL у дочерних объектов'''
        if not self.id:
            raise ValueError("У объекта еще нет ID")

        subitems = Menu.objects.filter(parent_id = self.id).only('alias')

        if not subitems:
            return False

        path = self.get_url_path(self.alias)
        urls = {}
        for subitem in subitems:
            urls.update({str(subitem.id) :  path + subitem.alias})

        with transaction.atomic():
            for key, value in urls.items():
                item = Menu.objects.get(id=key)
                item.url = value
                item.save(update_fields=['url'], lock_recursion=True)

        for subitem in subitems:
            subitem.update_urls()


    def get_url_path(self, path=''):
        '''формирует URL объекта'''
        if self.parent_id:
            parent = Menu.objects.get(id=self.parent_id)
            path = parent.alias + '/' + path
            return parent.get_url_path(path)
        else:
            return '/'+ path + '/'


    # def update_order(self):
    #         '''обновляет порядок элементов с общим родителем'''
    #         # получаем соседние объекты
    #         menus = list(Menu.objects.filter(parent_id=self.parent_id).exclude(id=self.id))
    #         menus_count = len(menus)
    #         # формируем список новых ордеров
    #         orders = [i for i in range(1, menus_count + 1 + 1)]

    #         # если новый ордер за пределами возможных или равен 0
    #         if (self.order > menus_count + 1) or (self.order <= 0):

    #             with transaction.atomic():
    #                 # просто присваем последний ордер
    #                 self.order = orders[-1]
    #                 self.save(update_fields=['order'], lock_recursion=True)
    #                 # обновляем соседние меню
    #                 for i in orders[:-1]:
    #                     menus[i-1].order = i
    #                     menus[i-1].save(update_fields=['order'], lock_recursion=True)
                    
    #         else: # если новый ордер в пределах возможных
    #             # резервируем нужный ордер для изменяемого меню, другие меню расставляем по остальным ордерам
    #             obj_num = 0
    #             with transaction.atomic():
    #                 for i in orders:
    #                     if i != self.order:
    #                         menus[obj_num].order = i
    #                         menus[obj_num].save(update_fields=['order'], lock_recursion=True)
    #                         obj_num += 1

    def update_list_order(self, parent_id=None, start_order=1):
            '''обновляет порядок всех элементов при выводе списком'''
            # получаем соседние объекты
            menus = list(Menu.objects.filter(parent_id=parent_id).order_by('order'))
            if len(menus) == 0:
                return start_order

            new_order = start_order
            for obj in menus:
                obj.list_order = new_order
                obj.save(update_fields=['list_order'], lock_recursion=True)
                new_order = obj.update_list_order(parent_id=obj.id, start_order= new_order + 1)
            return new_order
                


    def update_subitems_level(parent):
        '''Обновляет уровень вложенности в дочерних пунктах меню'''
        if not parent.id:
            raise ValueError("У объекта еще нет ID")

        subitems = Menu.objects.filter(parent_id = parent.id)
        subitems.update(
            level=parent.level + 1
        )
        for subitem in subitems:
            subitem.update_subitems_level()

    def get_subitems(parent=None, maxlevel=None):
        '''формирует дерево дочерних элементов'''
        if parent:
            if maxlevel:
                # если достигнут порог уровня - выходим
                if parent.level >= maxlevel:
                    return None
            items = Menu.objects.filter(parent_id=parent.id, published=True)
        else:
            items = Menu.objects.filter(level=1, published=True)

        # если дочерних элементов нет - выходим
        if len(items) == 0:
            return None

        result = []
        for item in items:
            # url  = parent_url + item.alias + "/"
            result.append(
                {
                    'item': item,
                    'url': item.url,
                    'subitems': item.get_subitems(maxlevel=maxlevel)
                }
            )
        
        return result

    def leveled_title(self):
        if self.level > 1:
            return '|---' * (self.level - 1) + self.title
        else:
            return self.title

    def __str__(self):
        return self.leveled_title()

    class Meta:
        ordering = ['list_order']
        verbose_name = "Меню"
        verbose_name_plural = "Меню"