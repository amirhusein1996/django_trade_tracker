from django.urls import path
from .views import ContactUsCreateView,MessageReceivedTemplateView

app_name = 'contact_us_module'

urlpatterns = [
    path('get-in-touch/' , ContactUsCreateView.as_view() , name = 'contact_us_page'),
    path('massage-received/', MessageReceivedTemplateView.as_view() , name = 'massage_received' )
]