from tkinter import CASCADE
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from app.utils import slugify_rus

# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    alias = models.SlugField(blank=True,
                             max_length=100, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    parent = models.ForeignKey(
        'Menu', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родитель")
    is_fixed = models.BooleanField(default=False, verbose_name="Зафиксировать дочерние пункты меню?",
                                   help_text="Если отмечено - дочерние пункты меню не будут раскрываться, если не отмечено -  будут.")
    short_description = models.CharField(max_length=100, blank=True,
        verbose_name="Краткое описание", help_text="Краткое описание содержимого меню")
    description = RichTextUploadingField(verbose_name="Описание")

    def save(self, *args, **kwargs):
        # только при создании объекта, id еще не существует
        if not self.id:
            self.alias = slugify_rus(self.title)

        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Page(models.Model):
    menu_id = models.ForeignKey(
        'Menu', on_delete=models.CASCADE, verbose_name="Привязка к меню")

    title = models.CharField(max_length=1000, verbose_name="Заголовок")
    text = RichTextUploadingField()

    def __str__(self):
        return self.title
