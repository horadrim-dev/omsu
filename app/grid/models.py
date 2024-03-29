from turtle import position
from django.db import models, transaction
from django.db.models import Q
# from django.forms import ValidationError
from content.models import ContentLayout
from app.models import OrderedModel
from ckeditor_uploader.fields import RichTextUploadingField
from menus.models import Menu
import datetime
import uuid
# Create your models here.

class GridManager(models.Manager):

    def published_on_page(self, menu:Menu):
        self.filter()
        if self.model is Section:
            return self.filter(
                # Q(column__module__menu=menu) | Q(column__module__show_on_every_page=True),
                (Q(column__module__invert=True) & ~Q(column__module__menu=menu)) 
                    | (Q(column__module__invert=False) & Q(column__module__menu=menu)) 
                    | Q(column__module__show_on_every_page=True),
                column__module__published=True, 
                column__module__published_at__lte=datetime.date.today()
                ).distinct()
        elif self.model is Column:
            return self.filter(
                # Q(module__menu=menu) | Q(module__show_on_every_page=True),
                (Q(module__invert=True) & ~Q(module__menu=menu)) 
                | (Q(module__invert=False) & Q(module__menu=menu)) 
                | Q(module__show_on_every_page=True),
                module__published=True, 
                module__published_at__lte=datetime.date.today()
                ).distinct()
        elif self.model is Module:
            return self.filter(
                (Q(invert=True) & ~Q(menu=menu)) 
                | (Q(invert=False) & Q(menu=menu)) 
                | Q(show_on_every_page=True),
                # Q(menu=menu) | Q(show_on_every_page=True),
                published=True, 
                published_at__lte=datetime.date.today()
                )

class Base(models.Model):
    name = models.CharField(default="", max_length=100, verbose_name="Название")
    classes = models.CharField(max_length=256, verbose_name="CSS классы", blank=True, help_text="Можно использовать bootstrap классы.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    objects = GridManager()
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Section(Base, OrderedModel):

    indents = models.BooleanField(default=True, verbose_name="Отступы по бокам")

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"
        ordering = ['order']

    def has_columns(self):
        return True if len(Column.objects.filter(section=self.id)) > 0 else False


    def save(self, lock_recursion=False, *args, **kwargs):

        super(Base, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(Section.objects.all().exclude(id=self.id))
            )

        if not self.has_columns():
            Column(name="Колонка 1", section_id=self.id).save()

    def has_columns_with_modules(self):
        has = False
        for col in self.column_set.all():
            if col.has_published_modules():
                has = True
                break
        return has

class Column(Base, OrderedModel):
    section = models.ForeignKey('Section', verbose_name="Секция", on_delete=models.CASCADE)
    width = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name="Ширина блока", 
        help_text="Ширина экрана разделяется на 12 частей. В сумме с остальными блоками ширина не должна быть больше 12. Если оставить 0, ширина будет вычислена автоматически.")

    class Meta:
        verbose_name = "Колонка"
        verbose_name_plural = "Колонки"
        ordering = ['section', 'order']

    def save(self, lock_recursion=False, *args, **kwargs):
        # self.check_width()

        super(Column, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(Column.objects.filter(section=self.section).exclude(id=self.id))
            )

    def __str__(self):
        return '[{}/{}]: {}/{} '.format(self.section.order, self.order, self.section.name, self.name)

    def has_published_modules(self):
        return True if self.module_set.published().count() else False

class Module(Base, OrderedModel):
    menu = models.ManyToManyField('menus.Menu', verbose_name="Привязка к меню")
    invert = models.BooleanField(default=False, verbose_name="Инвертировать выбор меню",
        help_text="Модуль будет привязан ко всем меню, кроме отмеченных.")
    show_on_every_page = models.BooleanField(default=False, verbose_name="Отображать на всех страницах сайта",
        help_text="Если выбрано - значения из поля \"меню\" будут проигнорированы.")
    column = models.ForeignKey('grid.Column', verbose_name="Позиция", on_delete=models.CASCADE)
    show_title = models.BooleanField(default=True, verbose_name="Заголовок")
    standart_design = models.BooleanField(default=True, verbose_name="Оформление по умолчанию")
    centrize = models.BooleanField(default=False, verbose_name="Центрировать содержимое")
    published = models.BooleanField(default=True, verbose_name='Опубликовано')
    published_at = models.DateField(default=datetime.date.today, 
                                    verbose_name="Дата публикации")

    pre_html = RichTextUploadingField(default="", verbose_name="Текст в начале модуля", blank=True, null=True)
    post_html = RichTextUploadingField(default="", verbose_name="Текст в конце модуля", blank=True, null=True)

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"
        ordering = ['column', 'order']

    def save(self, lock_recursion=False, *args, **kwargs):
        # self.check_width()

        super(Module, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(Module.objects.filter(column=self.column).exclude(id=self.id))
            )


class ModuleContent(OrderedModel, ContentLayout):

    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="Модуль")

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ['order']

    def save(self, lock_recursion=False, *args, **kwargs):

        super(ModuleContent, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(ModuleContent.objects.filter(module=self.module).exclude(id=self.id))
            )

