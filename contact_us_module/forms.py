from django import forms
from django.forms import ClearableFileInput
from .models import ContactUsMessage

class ContactUsImageInput ( ClearableFileInput ):
    template_name = 'contact_us_module/components/_contact_us_image_input.html'

class ContactUsModelForm(forms.ModelForm):
    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)
        for field in self.fields:
            self.fields[field].label = ''
    class Meta:
        model = ContactUsMessage
        fields = ['subject' , 'image' , 'message']
        widgets={
            'subject':forms.TextInput(attrs={
                'class' : 'input1' ,
                'placeholder': 'Subject',
            }),
            'image':ContactUsImageInput(),
            'message' : forms.Textarea(attrs={
                'class' : 'input1' ,
                'placeholder' : 'Message'
            })
        }