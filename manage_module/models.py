from django.db import models
from django.db.models import Manager
from base_module.models.deletion import SoftDeletionModel , SoftDeletionManager
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator,MaxLengthValidator
from account_module.models import User
from django.utils.text import slugify


class TradeAccount(SoftDeletionModel):
    title = models.CharField(max_length=20,validators=[MinLengthValidator(3),MaxLengthValidator(20)])
    user = models.ForeignKey(User , on_delete=models.PROTECT)
    more_info =models.OneToOneField('MoreInfo', models.PROTECT)
    slug = models.SlugField(db_index=True ,blank=True,null=True, editable=False, unique=False)
    created_date = models.DateTimeField(auto_now_add=True , blank=True , null=True,editable=False)

    is_active = models.BooleanField(default=True)


    # class Meta:
    #     unique_together = ('user' , 'title')

    def save(self , *args , **kwargs) :
        self.slug = slugify(self.title)
        self.title= self.title.title()

        super().save(*args , **kwargs)

    def __str__(self):
        return self.title


class MoreInfoManager(SoftDeletionManager):
    def get_queryset(self):
        return super().get_queryset().using(self._db).exclude(tradeaccount__is_deleted=True)
class MoreInfo(SoftDeletionModel):
    balance = models.IntegerField(validators=[MinValueValidator(0)])
    profit_target = models.IntegerField(validators=[MinValueValidator(0)])
    daily_loss_limit = models.IntegerField(validators=[MinValueValidator(0)])
    overal_loss_limit = models.IntegerField(validators=[MinValueValidator(0)])
    minimum_trading_days = models.IntegerField(validators=[MinValueValidator(0)])
    days_traded = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.balance)
    def clean(self):
        if self.daily_loss_limit > self.overal_loss_limit:
            raise ValidationError("Daily Loss Limit Can't be greater than Overal Loss Limit")
        if self.daily_loss_limit > self.balance or self.overal_loss_limit > self.balance:
            raise ValidationError("Cant lose money more than Balance")

    objects = MoreInfoManager()