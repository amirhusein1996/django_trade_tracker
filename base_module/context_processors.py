from django.http import HttpRequest
from account_module.models import UserExtraInformations
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


' Used as a component'
@method_decorator(login_required, name='dispatch')
class UserProfile(DetailView):
    template_name = 'account_module/components/_user_profile.html'
    context_object_name = 'user'
    model = UserExtraInformations

    def get_object(self, queryset=None):
        user_info = get_object_or_404(klass=self.model ,user = self.request.user)
        return user_info
    def render_to_response(self, context, **response_kwargs):
        return render_to_string(template_name=self.template_name, context=context)


def user_profile(request:HttpRequest):
    if request.user.is_authenticated:
        view = UserProfile.as_view()
        user_profile = view(request)

        return {
            'user_profile' : user_profile
        }