from django.forms import ModelForm
from .models import Attachment, Post

from django.forms.models import inlineformset_factory, BaseInlineFormSet
# Create the form class.
class AdminPostForm(ModelForm):
    class Meta:
        model = Post
        # конкретно выбрать отображаемые поля
        # fields = ['pub_date', 'headline', 'content', 'reporter']
        # исключить поля
        exclude = []

# AttachmentFormset = inlineformset_factory(Post, Attachment, extra=1)
