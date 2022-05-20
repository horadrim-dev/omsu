from ast import arg
from django.db import models
from menus.models import Menu
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from app.utils import slugify_rus

# Create your models here.
class Content(models.Model):


    title = models.CharField(default="", max_length=1000, verbose_name="Заголовок")
    alias = models.SlugField(default="", blank=True, 
                             max_length=1000, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")

    def save(self, lock_recursion=False, *args, **kwargs):
        # только при создании объекта, id еще не существует
        if not self.id:
            if not self.alias:
                # заполняем алиас
                self.alias = slugify_rus(self.title)

        super(Content, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Feed(Content):

    menu = models.ManyToManyField(Menu, verbose_name="Привязка к меню")
    description = RichTextUploadingField()


class Post(Content):

    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, verbose_name="Привязка к меню", blank=True, null=True)
    feed = models.ManyToManyField(Feed, blank=True, verbose_name="Категория")
    text = RichTextUploadingField()

class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    name = models.CharField(default="", max_length=1000, verbose_name="Название")
    # file_type = models.CharField(default="", max_length=100, blank=True, verbose_name="Формат файла")
    attachment = models.FileField(upload_to='attachments/', blank=True, verbose_name='Вложение')