from django import forms
from account_module.models import UserExtraInformations
from django.forms import ClearableFileInput

class UserAvatarWidget(ClearableFileInput):
    template_name = 'account_module/components/_update_profile_image_input.html'

class UpdateProfileModelForm (forms.ModelForm):

    class Meta:
        model = UserExtraInformations
        exclude = ['user']

        widgets = {
            'first_name' : forms.TextInput (attrs={'placeholder': 'First Name' , 'class' : 'name-input', 'id' : 'first_name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class' : 'name-input' , 'id':"last_name"}),
            'gender': forms.Select(attrs={
                'class': 'gender-input' , 'id': 'gender'
            }) ,
            'birthdate': forms.DateInput(attrs={'type': 'date' , 'class':'birthdate-input' , 'id': 'birthdate'}),
            'avatar': UserAvatarWidget(),
        }

