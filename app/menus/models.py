from tkinter import CASCADE
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    alias = models.SlugField(blank=True,
        max_length=100, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'. Чем короче тем лучше.")
    parent = models.ForeignKey(
        'Menu', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родитель")
    is_fixed = models.BooleanField(default=False, verbose_name="Раскрывать дочерние пункты меню?",
                                   help_text="Если отмечено - дочерние пункты меню будут раскрываться, если нет - не будут.")
    description = models.TextField(
        verbose_name="Описание", help_text="Краткое описание содержимого меню")

    def __str__(self):
        return self.title


class Page(models.Model):
    menu_id = models.ForeignKey(
        'Menu', on_delete=models.CASCADE, verbose_name="Привязка к меню")

    title = models.CharField(max_length=1000, verbose_name="Заголовок")
    text = RichTextUploadingField()

    def __str__(self):
        return self.title
