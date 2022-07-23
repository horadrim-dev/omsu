from django import forms
from .models import Module

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        # fields = []
        exclude = []

    def clean(self):
        cleaned_data = super(ModuleForm, self).clean()

        if cleaned_data:
            if cleaned_data.get('invert') and  cleaned_data.get('show_on_every_page'):
                msg = 'Одновременное инвертирование и показ на всех страницах не будут работать. Уберите одну из опций.'
                self.add_error('invert', msg)
                self.add_error('show_on_every_page', msg)

