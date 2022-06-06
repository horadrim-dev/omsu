from django.db import models, transaction
from django.forms import ValidationError
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
        ordering = ['order']

    def save(self, lock_recursion=False, *args, **kwargs):

        super(Base, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(Section.objects.all().exclude(id=self.id))
            )


class Block(Base, OrderedModel):
    section = models.ForeignKey('Section', verbose_name="Секция", on_delete=models.CASCADE)
    width = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name="Ширина блока", 
        help_text="Ширина экрана разделяется на 12 частей. В сумме с остальными блоками ширина не должна быть больше 12. Если оставить 0, ширина будет вычислена автоматически.")

    class Meta:
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"
        ordering = ['order']

    def save(self, lock_recursion=False, *args, **kwargs):
        # self.check_width()

        super(Block, self).save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(Block.objects.filter(section=self.section).exclude(id=self.id))
            )

    # def check_width(self):
    #     sum_width = self.width
    #     blocks = Block.objects.filter(section=self.section).only('width').exclude(id=self.id)
    #     for block in blocks:
    #         sum_width += block.width

    #     if sum_width > 12:
    #         raise ValidationError('Суммарная ширина всех блоков в секции не должна превышать 12, ({}>12)'.format(sum_width))
    #     else:
    #         return True

