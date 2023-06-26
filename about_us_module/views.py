from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import AboutUs

class AboutUsDetailView(DetailView):
    template_name = 'about_us_module/about_us_page.html'
    model = AboutUs


    def get_object(self, queryset=None):
        return get_object_or_404(self.model , is_active = True)
