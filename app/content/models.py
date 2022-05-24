# from ast import arg
# from re import A
# from tabnanny import verbose
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from menus.models import Menu
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from app.utils import slugify_rus
import datetime
import os
import uuid
# Create your models here.


def attachment_upload_location(instance, filename):
    '''Задает путь для сохранения вложений'''
    # _ , extension = os.path.splitext(filename)
    filename = '%s.%s' % (slugify_rus(instance.name), instance.extension)
    # assert False, '2' + filename
    path = 'attachments/'
    # если у поста есть привязка к меню, сохраняем с аналогичной меню директорией
    if instance.post.menu:
        return path + '{}/{}'.format(instance.post.menu.url, filename)

    # если привязки к меню нет, то сохраняем в директорию feeds/feed_alias
    if instance.post.feed:
        return path + '{}/{}/{}/{}'.format(
            'feeds/', 
            instance.post.feed.alias, 
            instance.date_publish.strftime('/%Y/%m/%d/'), 
            filename
        )

    return False

class Content(models.Model):

    title = models.CharField(
        default="", max_length=1000, verbose_name="Заголовок")
    alias = models.SlugField(default="", blank=True, unique=True,
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
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, verbose_name="Лента постов", blank=True, null=True)
    # feed = models.ManyToManyField(Feed, blank=True, verbose_name="Лента")
    text = RichTextUploadingField()


class Attachment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    name = models.CharField(default="", max_length=1000,
                            verbose_name="Название")
    extension = models.CharField(default="", max_length=16, blank=True, 
                                verbose_name="Расширение файла")
    attached_file = models.FileField(upload_to=attachment_upload_location, 
                                    verbose_name='Вложение')
    date_publish = models.DateField(default=datetime.date.today, 
                                    verbose_name="Дата публикации")
    hits = models.PositiveIntegerField(default=0, verbose_name="Кол-во загрузок")

    def __str__(self):
        return self.name
    
    def url(self):
        '''Формирует url для скачивания'''
        return reverse('attachment_download', kwargs={'uuid': self.uuid})

    def save(self,  *args, **kwargs):
        # считываем расширение файла
        self.extension = self.attached_file.path.split('.')[-1].lower()
        # assert False, '1' + self.extension
        return super(Attachment, self).save(*args, **kwargs)

@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Удаляет файл при удалении объекта вложения
    """
    if instance.attached_file:
        if os.path.isfile(instance.attached_file.path):
            os.remove(instance.attached_file.path)