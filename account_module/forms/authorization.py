from django import forms
from django.core.validators import EmailValidator , MinLengthValidator

class SignUpForm(forms.Form):

    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'placeholder':'Email',
            'name':'email'
        }),
        validators=[EmailValidator],
        label=""
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'name': 'password'
        }),
        validators=[MinLengthValidator(limit_value=8 ,
        message="Your password must be at least 8 charecters")],
        label=""
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'name': 'confirm_password'
        }),
        label = ""
    )

    def clean_confirm_password(self):
        from django.core.exceptions import ValidationError

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Both the password and confirm password must be matched!')
        return confirm_password

    def clean_email(self):
        from django.core.exceptions import ValidationError
        import re

        email = self.cleaned_data['email']
        
        email_pattern = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        regex = re.compile(email_pattern)

        if re.fullmatch(regex , email ):
            return email
        raise ValidationError('Email is not valid')



class SingInForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'placeholder':'Email',
            'name':'email'
        }),
        validators=[EmailValidator],
        label="",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'name': 'password'
        }),
        label="",
    )


    def clean_email(self):
        from django.core.exceptions import ValidationError
        import re

        email = self.cleaned_data['email']

        email_pattern = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        regex = re.compile(email_pattern)

        if re.fullmatch(regex, email):
            return email
        raise ValidationError('Email is not valid')

class ResetPasswordForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'placeholder':'Email',
            'name':'email'
        }),
        validators=[EmailValidator],
        label="",
    )

    def clean_email(self):
        from django.core.exceptions import ValidationError
        import re

        email = self.cleaned_data['email']

        email_pattern = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        regex = re.compile(email_pattern)

        if re.fullmatch(regex, email):
            return email
        raise ValidationError('Email is not valid')


