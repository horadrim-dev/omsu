from django import forms
from .models import Content

# from django.forms.models import inlineformset_factory, BaseInlineFormSet

# Create the form class.
# class AdminPostForm(ModelForm):
#     class Meta:
#         model = Post
#         # конкретно выбрать отображаемые поля
#         # fields = ['title', 'alias', 'published', 'published_at']
#         # исключить поля
#         exclude = []

# AttachmentFormset = inlineformset_factory(Post, Attachment, extra=1)

class ContentForm(forms.ModelForm):

    class Meta:
        model = Content
        # fields = []
        exclude = []
    
    class Media:
        js = ('content/js/content_form.js',)

    def clean(self):
        # cleaned_data = super(WidgetForm, self).clean()
        if not self.is_valid():
            return #other errors exist, so don't bother
        if self.cleaned_data:
            if self.cleaned_data.get('content_type') == 'menu' and not self.cleaned_data.get('content_menu'):
                # raise ValidationError('Поле "Меню" обязательно для заполнения!');
                self.add_error('content_menu', 'Поле "Меню" обязательно для заполнения!')
            if self.cleaned_data.get('content_type') == 'feed' and not self.cleaned_data.get('content_feed'):
                # raise ValidationError('Поле "Лента постов" обязательно для заполнения!');
                self.add_error('content_feed', 'Поле "Лента постов" обязательно для заполнения!')
            if self.cleaned_data.get('content_type') == 'post' and not self.cleaned_data.get('content_post'):
                # raise ValidationError('Поле "Пост" обязательно для заполнения!');
                self.add_error('content_post', 'Поле "Пост" обязательно для заполнения!')