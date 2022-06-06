from django.db import models, transaction
from app.models import OrderedModel
# Create your models here.

class Base(models.Model):
    name = models.CharField(default="", max_length=100, verbose_name="Название")
    classes = models.CharField(max_length=256, verbose_name="CSS классы",blank=True, help_text="Можно использовать bootstrap классы.")
    background = models.CharField(default="ffffff", max_length=6)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Section(Base, OrderedModel):

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"

    def save(self, lock_recursion=False, *args, **kwargs):

        super(Base, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(Section.objects.all().exclude(id=self.id))
            )

    class Meta:
        ordering = ['order']


class Block(Base, OrderedModel):
    section = models.ForeignKey('Section', verbose_name="Секция", on_delete=models.CASCADE)