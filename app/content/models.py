from django.db import models
from menus.models import Menu
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, verbose_name="Привязка к меню")

    title = models.CharField(max_length=1000, verbose_name="Заголовок")
    text = RichTextUploadingField()

    def __str__(self):
        return self.title