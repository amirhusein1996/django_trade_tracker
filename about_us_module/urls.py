from django.urls import path
from .views import AboutUsDetailView

app_name = 'about_us_module'

urlpatterns=[
    path('' , AboutUsDetailView.as_view() , name='about_us_page'),
]