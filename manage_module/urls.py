from django.urls import path
from . import views

app_name = 'manage_module'

urlpatterns = [
    path('manage-trade-accounts/' , views.TradeAccountManagement.as_view() , name = 'manage_page'),

    # ajax
    path('ajax-requests/edit/trade-accounts/', views.UpdateTradeAccount.as_view(), name='edit_trade_account'),
    path('ajax-requests/create/create-trade-account/', views.CreateNewTradeAccountFormView.as_view() , name = 'create_trade_account'),
    path("ajax-requests/manage-trade-accounts/is-active/" ,views.IsActive.as_view() , name= "is_active"),
    path("ajax-requests/manage-trade-accounts/is-delete/" , views.IsDelete.as_view(), name = "delete_trade_account"),
]
