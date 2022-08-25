from taggit_labels.widgets import LabelWidget
from .models import Tag


class TaggedPostLabelWidget(LabelWidget):
    '''
    Класс модуля django-taggit-labels. Необходимо потому что он напрямую привязан
    к родному тегу. Переопределение позволяет использовать кастомный тег.

    '''
    model = Tag