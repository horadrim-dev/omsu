from logging import PlaceHolder
from django import forms
from .models import ExtraContent
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
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



class ExtraContentForm(forms.ModelForm):

    class Meta:
        model = ExtraContent
        # fields = []
        exclude = []
    
    class Media:
        js = ('content/js/extracontent_form.js',)

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


class FeedFilterForm(forms.Form):
    template_name = 'content/layout_feed_filter.html'
    q = forms.CharField(
        label="Содержит", 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class':"form-control", 
                'placeholder':'Введите фразу для поиска',
            }
        )
    )
    date_start = forms.DateField(
        label='с',
        widget=DateTimePickerInput(format="%d.%m.%Y",)
    )
    date_end = forms.DateField(
        label='по',
        widget=DateTimePickerInput(format="%d.%m.%Y",)
    )
    # max_date = forms.DateField(
    #     widget=forms.DateInput(
    #         attrs={'class':"form-control", 'placeholder':'Дата'}
    #     )
    # )