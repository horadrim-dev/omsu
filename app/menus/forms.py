from django.forms import ModelForm
from .models import Menu

# Create the form class.
class AdminMenuForm(ModelForm):
    class Meta:
        model = Menu
        # конкретно выбрать отображаемые поля
        # fields = ['pub_date', 'headline', 'content', 'reporter']
        # исключить поля
        exclude = ['level']