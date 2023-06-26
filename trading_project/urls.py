"""trading_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from base_module.views.base import reditector
from django.conf import settings


urlpatterns = [
    path('' ,reditector , name= 'redirector'),
    path("admin/", admin.site.urls),
    path('accounts/' , include('account_module.urls' , namespace='account_module')) ,
    path('home/',include('home_module.urls',namespace='home')),
    path('manage/' , include('manage_module.urls' , namespace='manage_module')),
    path('base/' , include('base_module.urls' , namespace='base_module')) ,
    path('contact-us/' , include('contact_us_module.urls' , namespace='contact_us_module')),
    path('about-us/' , include('about_us_module.urls' , namespace='about_us_module')),
    path('requests/' , include('request_limitation.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)