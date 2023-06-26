from django.shortcuts import redirect , reverse
from account_module.models import User , UserExtraInformations
from django.template.loader import render_to_string
from django.views.generic import DetailView , UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST, require_http_methods


from account_module.forms.base import UpdateProfileModelForm
from django.shortcuts import get_object_or_404


' Used as a component'
@method_decorator(login_required, name='dispatch')
class UserProfile(DetailView):
    template_name = 'account_module/components/_user_profile.html'
    context_object_name = 'user'
    model = UserExtraInformations

    def get_object(self, queryset=None):
        user_id = self.request.user.pk
        user , created = self.model.objects.get_or_create(user_id=user_id)
        return user
    def render_to_response(self, context, **response_kwargs):
        return render_to_string(template_name=self.template_name, context=context)

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView ( UpdateView):
    template_name = 'account_module/edit_profile.html'
    model = UserExtraInformations
    form_class = UpdateProfileModelForm
    context_object_name = 'user'
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args , **kwargs)
        user = context['user']
        user_profile = render_to_string(template_name='account_module/components/_user_profile.html' ,
                                        context={'user':user})
        context['user_profile'] = user_profile
        return context

    def get_object(self, queryset=None):
        user_id = self.request.user
        return get_object_or_404(self.model , user = user_id)
    def form_valid(self, form):
        form.save()
        return redirect(reverse('home:index'))


