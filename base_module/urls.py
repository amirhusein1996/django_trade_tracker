from django.urls import path
from base_module.views.base import get_home_and_manage_urls

app_name = 'base_module'

urlpatterns = [
    path('ajax-requests/get/home_and_manage_urls/' , get_home_and_manage_urls , name = 'home_and_manage_urls'),
]