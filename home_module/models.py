from django.db import models
from django.db.models import Prefetch
from base_module.models.deletion import SoftDeletionModel , SoftDeletionManager
from django.core.validators import MinValueValidator
from manage_module.models import TradeAccount , MoreInfo

class TradeRecordManager(SoftDeletionManager):
    def get_queryset(self):
        return super().get_queryset().using(self._db).select_related('currency_type').exclude(trade_account__is_deleted=True)

class TradeRecord(SoftDeletionModel):
    trade_account= models.ForeignKey(TradeAccount, on_delete=models.PROTECT)
    currency_type = models.ForeignKey(to = 'CurrencyType',on_delete=models.PROTECT)
    time = models.DateTimeField(blank=True,null=True)
    lot = models.DecimalField(max_digits=15, decimal_places=4,validators=[MinValueValidator(0)])
    sl=models.DecimalField(max_digits=15 ,decimal_places=4,validators=[MinValueValidator(0)])
    tp = models.DecimalField(max_digits=15, decimal_places=4,validators=[MinValueValidator(0)])
    r_r = models.DecimalField(max_digits=15, decimal_places=4, editable=False , blank=True, null=True)
    profit = models.DecimalField(max_digits=15, decimal_places=4)
    image = models.ImageField(upload_to='images/trade_accounts/account_detail', blank=True,null=True)
    description = models.TextField(blank=True,null=True)


    def __str__(self):
        return f"Currency type: {self.currency_type} with profit: {self.profit}"

    def save(self , *args , **kwargs):
        self.r_r= self.tp / self.sl if self.sl else 0
        if not self.time:
            from django.utils import timezone
            self.time = timezone.now()
        #Goal : override traded_days in MoreInfo
        if self.is_deleted == True:
            trade_account = TradeAccount.objects.select_related('more_info').prefetch_related(
                Prefetch('traderecord_set' ,queryset=TradeRecord.objects.exclude(id = self.id))
                ).get(id = self.trade_account.id, is_active=True)
        else:
            trade_account = TradeAccount.objects.select_related('more_info').prefetch_related('traderecord_set').get(id = self.trade_account.id, is_active=True)
        trade_records = trade_account.traderecord_set.all()

        time_set = {object.time.date() for object in trade_records}
        if self.is_deleted != True:
            time_set.add(self.time.date())

        more_info_instance = trade_account.more_info
        more_info_instance.days_traded = len(time_set)
        more_info_instance.save()
        #end of desired goal

        super().save(*args,**kwargs)

    objects = TradeRecordManager()

class CurrencyType(models.Model):
    currency_name = models.CharField(max_length=20 , unique=True)
    order_index = models.IntegerField(db_index=True)

    def save(self , *args , **kwargs):
        self.value = self.value.capitalize()
        super().save(*args , **kwargs)

    def __str__(self):
        return self.currency_name

class TimeInterval(models.Model):
    value = models.CharField(max_length=20)
    to_show = models.CharField(max_length=20)
    order_index = models.IntegerField(db_index=True)

    def save(self , *args , **kwargs):
        self.to_show = self.to_show.title()
        super().save(*args , **kwargs)

    def __str__(self):
        return self.to_show






