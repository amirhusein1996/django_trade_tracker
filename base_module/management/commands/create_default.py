from django.core.management.base import BaseCommand
from django.core.management import call_command
from home_module.models import CurrencyType,TimeInterval


class Command(BaseCommand):
    help = "to create default instances of CurrencyType and TimeInterval"

    def handle(self, *args, **options):
        ct_count = CurrencyType.objects.count()
        ti_count = TimeInterval.objects.count()
        if ct_count == 0 :
            default_objects =[
                CurrencyType(currency_name="EURO/USD",order_index=1),
                CurrencyType( currency_name="GBP/USD", order_index=2),
                CurrencyType(currency_name="XAU/USD", order_index=3),
                CurrencyType(currency_name='US30', order_index=4),
                CurrencyType( currency_name='US100', order_index=5),
                CurrencyType(currency_name='US500', order_index=6),
                CurrencyType( currency_name='USD/CAD', order_index=7),
                CurrencyType(currency_name="USD/JPY", order_index=8),
                CurrencyType( currency_name='USD/CHF', order_index=9),
                CurrencyType(currency_name="AUD/USD", order_index=10),
                CurrencyType( currency_name='NZD/USD', order_index=11),
                CurrencyType( currency_name='EURO/GBP', order_index=12),
                CurrencyType( currency_name='EURO/JPY', order_index=13),
                CurrencyType( currency_name='EURO/CHF', order_index=14),
                CurrencyType(currency_name='GBPJPY', order_index=15),
                CurrencyType( currency_name='EURO/CAD', order_index=16),
                CurrencyType( currency_name='GBPCAD', order_index=17),
                CurrencyType(currency_name='AUD/CAD', order_index=18),
                CurrencyType(currency_name='NZD/CAD', order_index=19),
                CurrencyType( currency_name='BTC/USD', order_index=20),
                CurrencyType( currency_name='ETH/USD', order_index=21),
                CurrencyType( currency_name='ADA/USD', order_index=22),
                CurrencyType( currency_name='XAG/USD', order_index=23),
                CurrencyType(currency_name='WTI', order_index=24),
                CurrencyType( currency_name='F40', order_index=25),
                CurrencyType(currency_name='DXA', order_index=26),
                CurrencyType(currency_name='USOIL', order_index=27),
            ]

            CurrencyType.objects.bulk_create(default_objects)

        if ti_count == 0:
            default_objects = [
                TimeInterval(value='all', to_show='All', order_index=1),
                TimeInterval(value='yearly', to_show='Yearly', order_index=2),
                TimeInterval(value='six-months', to_show='6 months', order_index=3),
                TimeInterval(value='monthly', to_show='Monthly', order_index=4),
                TimeInterval(value='weekly', to_show='Weekly', order_index=5),
                TimeInterval(value='daily', to_show="Daily", order_index=6),
                TimeInterval(value='four-hours', to_show="4 Hours", order_index=7),
                TimeInterval(value='one-hour', to_show='1 Hour', order_index=8),
            ]
            TimeInterval.objects.bulk_create(default_objects)
