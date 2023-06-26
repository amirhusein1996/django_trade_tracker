from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.index , name='index' ),
    path('download/download-chart/', views.DownloadTradeChartView.as_view(), name="download_chart"),

    # ajax
    path('ajax-requests/get/trade-list/', views.TradeListAjax.as_view(), name='get_trade_record_list'),
    path('ajax-requests/get/trade-overview/', views.TradeOverviewAjax.as_view(), name='get_trade_overview'),

    path('ajax-requests/edit/update-note/',views.UpdateNoteUpdateView.as_view(),name = 'update_note'),
    path('ajax-requests/delete/trade-record/', views.DeleteTradeRecord.as_view(), name='delete_trade_record'),
    path('ajax-requests/create/create-trade-record/', views.TradeRecordCreateView.as_view(), name='create_trade_record'),
]

