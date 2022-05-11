from ast import arg
from django.db import models
from menus.models import Menu
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from app.utils import slugify_rus

# Create your models here.

class Feed(models.Model):

    menu = models.ManyToManyField(Menu, verbose_name="Привязка к меню")

    title = models.CharField(max_length=1000, verbose_name="Заголовок")
    alias = models.SlugField(default="", blank=True, unique=True,
                             max_length=1000, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    description = RichTextUploadingField()

    def __str__(self):
        return self.title

    def save(self, lock_recursion=False, *args, **kwargs):
        # только при создании объекта, id еще не существует
        if not self.id:
            if not self.alias:
                # заполняем алиас
                self.alias = slugify_rus(self.title)

        super(Feed, self).save(*args, **kwargs)


class Post(models.Model):

    title = models.CharField(max_length=1000, verbose_name="Заголовок")
    alias = models.SlugField(default="", blank=True, 
                             max_length=1000, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, verbose_name="Привязка к меню", blank=True, null=True)
    feed = models.ManyToManyField(Feed, blank=True, null=True, verbose_name="Категория")
    text = RichTextUploadingField()

    def __str__(self):
        return self.title

    def save(self, lock_recursion=False, *args, **kwargs):
        # только при создании объекта, id еще не существует
        if not self.id:
            if not self.alias:
                # заполняем алиас
                self.alias = slugify_rus(self.title)

        # if not self.menu_id and not self.feed:
        #     raise Exception('OMG!')

        super(Post, self).save(*args, **kwargs)