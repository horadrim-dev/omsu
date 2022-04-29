from tkinter import CASCADE
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from app.utils import slugify_rus
# from django.db.models import F

# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    alias = models.SlugField(blank=True, unique=True,
                             max_length=100, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    parent = models.ForeignKey(
        'Menu', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родитель")
    level = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    is_fixed = models.BooleanField(default=False, verbose_name="Зафиксировать дочерние пункты меню?",
                                   help_text="Если отмечено - дочерние пункты меню не будут раскрываться, если не отмечено -  будут.")
    icon = models.CharField(max_length=32, default="", blank=True, verbose_name="Иконка", help_text="Необязательно. Названия брать <a href='https://icons.getbootstrap.com/' target='_blank'>отсюда.</a>")
    short_description = models.CharField(max_length=100, blank=True,
        verbose_name="Краткое описание", help_text="Краткое описание содержимого меню")
    description = RichTextUploadingField(verbose_name="Описание", blank=True)

    def save(self, *args, **kwargs):
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
        
        super(Menu, self).save(*args, **kwargs)

        # обновляем дочерние объекты
        self.rec_update_subitems_level()

    def rec_update_subitems_level(parent):
        '''Обновляет уровень вложенности в дочерних пунктах меню'''
        if not parent.id:
            raise ValueError("У объекта еще нет ID")

        subitems = Menu.objects.filter(parent_id = parent.id)
        subitems.update(
            level=parent.level + 1
        )
        for subitem in subitems:
            subitem.rec_update_subitems_level()

    def get_subitems(parent=None, maxlevel=None):
        '''формирует дерево дочерних элементов'''
        if parent:
            if maxlevel:
                if parent.level >= maxlevel:
                    return None
            items = Menu.objects.filter(parent_id=parent.id, is_published=True)
        else:
            items = Menu.objects.filter(level=1, is_published=True)

        if len(items) == 0:
            return None

        result = []
        for item in items:
            result.append(
                {
                    'item':item,
                    'subitems': item.get_subitems(maxlevel=maxlevel)
                }
            )
        
        return result

    def __str__(self):
        return self.title


class Page(models.Model):
    menu_id = models.ForeignKey(
        'Menu', on_delete=models.CASCADE, verbose_name="Привязка к меню")

    title = models.CharField(max_length=1000, verbose_name="Заголовок")
    text = RichTextUploadingField()

    def __str__(self):
        return self.title
