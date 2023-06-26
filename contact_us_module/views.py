from django.views.generic import CreateView , TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import ContactUsMessage
from .forms import ContactUsModelForm
from account_module.views.base import UserProfile

class ContactUsCreateView(CreateView):
    template_name = 'contact_us_module/contact_us_page.html'
    form_class = ContactUsModelForm
    success_url = reverse_lazy('contact_us_module:massage_received')

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return redirect(self.success_url)

class MessageReceivedTemplateView(TemplateView):
    template_name = 'contact_us_module/massage_received.html'
