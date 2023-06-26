from django import forms
from django.forms.widgets import ClearableFileInput
from home_module.models import TradeRecord

class TradeRecordModelForm(forms.ModelForm):
    account_name = forms.SlugField(max_length=20)
    currency_name= forms.CharField(max_length=20)
    class Meta:
        model = TradeRecord
        exclude = "trade_account" , "r_r" , 'image' , 'description','currency_type'


class ImagePreviewWidget(ClearableFileInput):
    template_name = 'home_module/components/_add_note_image_preview.html'

class UpdateNoteModelForm(forms.ModelForm):
    class Meta:
        model = TradeRecord
        fields = ['image' , 'description']
        widgets={
            'image':ImagePreviewWidget
        }