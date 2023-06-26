from django import forms
from manage_module.models import TradeAccount , MoreInfo
from django.core.validators import MinLengthValidator,MaxLengthValidator


class TradeAccountModelForm(forms.ModelForm):
    title = forms.CharField(max_length=20,validators=[MinLengthValidator(3,'Title is at least 3 letters'),MaxLengthValidator(20,'Title maximum lenght is 20')],
                            widget=forms.TextInput(attrs={
        'placeholder':'Title'
    }),
                            label='')
    slug = forms.SlugField(widget=forms.TextInput(attrs={'type':'hidden'}), required=False)
    class Meta:
        model = MoreInfo
        fields = ['title' , 'balance' , 'profit_target','daily_loss_limit','overal_loss_limit','minimum_trading_days','slug']
        widgets= {
            'title':                                 forms.TextInput(attrs={'placeholder': 'Title'}),
            'balance':                           forms.NumberInput(attrs={'placeholder': 'Balance'}),
            'profit_target':               forms.NumberInput(attrs={'placeholder': 'Profit Target'}),
            'daily_loss_limit':        forms.NumberInput(attrs={'placeholder': 'Dailiy Loss Limit'}),
            'overal_loss_limit':       forms.NumberInput(attrs={'placeholder': 'Overal Loss Limit'}),
            'minimum_trading_days':forms.NumberInput(attrs={'placeholder': ' Minimum Trading Days'})

        }
        # labels={
        #     field.name : '' for field in model._meta.fields #set empty all labels
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'


class IsActiveModelForm(forms.ModelForm):
    class Meta:
        model = TradeAccount
        fields = 'is_active' ,
