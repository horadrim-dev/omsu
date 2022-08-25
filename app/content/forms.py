from django import forms
from .models import ExtraContent, Post, Tag
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
import datetime
from taggit.forms import TagField
from .widgets import TaggedPostLabelWidget
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


class PostForm(forms.ModelForm):
    tags = TagField(required=False, widget=TaggedPostLabelWidget)
    class Meta:
        model = Post
        # fields = []
        exclude = ['intro_text']
        # widgets = {
        #     'tags': forms.TextInput(attrs={'data-role' : "tagsinput"})
        # }

    # class Media:
    #     js = (
    #         # 'app/js/bootstrap.bundle.min.js', 
    #         'app/js/typeahead.bundle.min.js', 
    #         'app/js/bootstrap-tagsinput.min.js',)
        # css = ('app/css/bootstrap-tagsinput.css')

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


class FeedValidationForm(forms.Form):

    page = forms.IntegerField(required=False) # отсутствует в шаблоне, нужен для валидации get

class FeedFilterForm(forms.Form):
    template_name = 'content/form_filter_feed.html'

    q = forms.CharField(
        label="Заголовок", 
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class':"form-control", 
                'placeholder':'Введите текст для поиска',
                }
            )
        )

    date_start = forms.DateField(
        label='Дата публикации (от)',
        required=False,
        widget=DateTimePickerInput(
            format="%d.%m.%Y",
            options={
                'locale':'ru',
                'showClose': False, 'showClear':True, 'showTodayButton':False
            }
        )
    )
    date_end = forms.DateField(
        label='(до)',
        required=False,
        widget=DateTimePickerInput(
            format="%d.%m.%Y",
            options={
                'locale':'ru',
                'showClose': False, 'showClear':True, 'showTodayButton':False
            }
        )
    )
    # tags = TagField(required=False, widget=TaggedPostLabelWidget)
    tag = forms.ModelChoiceField(
        label='Тег',
        required=False,
        queryset=Tag.objects
        # widget=TaggedPostLabelWidget()
    )
    # max_date = forms.DateField(
    #     widget=forms.DateInput(
    #         attrs={'class':"form-control", 'placeholder':'Дата'}
    #     )
    # )