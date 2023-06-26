from django.shortcuts import render , redirect , reverse , Http404
from django.views.generic import View  , TemplateView ,FormView, DetailView
from account_module.forms.authorization import SignUpForm,SingInForm , ResetPasswordForm
from account_module.models import User , UserExtraInformations
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods , require_POST, require_GET
class SentEmailMessageTemplateView(TemplateView):
    template_name = 'account_module/extends/_register_email_sent_message.html'


@method_decorator(require_http_methods(['GET' , 'POST']), name="dispatch")
class CreateAccount(View):
    template_name = 'account_module/extends/_create-account.html'
    form_class= SignUpForm

    def get(self , request):
        form = self.form_class()
        context = {
            'form' : form
        }
        return render(request , self.template_name,context )

    def post(self , request):
        from utils.activation_code import create_activation_code
        from  django.utils import timezone
        form = self.form_class(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            email :str = cd['email']
            password = cd['password']

            is_user: bool = User.objects.filter(email__iexact=email).exists()

            if not is_user:

                user : User = User.objects.create_user(email=email.lower(), password= password )
                user.activation_code= create_activation_code()
                user.activation_code_created_date = timezone.now()
                user.save()
                #todo: send activation code to user email
                return redirect(reverse("account_module:sent_email_message"))
            else:
                form.add_error('email', 'this email is already taken')
        return render(request , self.template_name , context={'form' : form})

@method_decorator(require_http_methods(['GET' , 'POST']), name="dispatch")
class Login(View):
    template_name = 'account_module/extends/_login.html'
    form_class = SingInForm

    def get(self , request):
        form = self.form_class()
        context = {
            'form' : form
        }
        return render(request , self.template_name ,context)

    def post(self , request):
        from django.contrib.auth import authenticate ,login
        form = self.form_class(data=request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            email=cd['email']
            password = cd['password']

            user :User = authenticate(email=email , password=password)
            if user :
                if user.is_active==True and user.is_banned == False :
                    login(request, user)
                    return redirect(reverse('home:index'))
            #todo : limit the login tries
            form.add_error('email', 'Email or Password is not correct or may not be actived,try again')
        return render(request , self.template_name , {'form':form})


class ActiveUser(View):
    template_name = 'account_module/extends/_active_account.html'
    def get(self,request , activate_code):
        from utils.activation_code import create_activation_code
        from django.utils import timezone

        user: User = User.objects.filter(activation_code__iexact=activate_code).first()
        if user is not None:
            if not user.is_banned:
                user.is_active = True
                user.activation_code = create_activation_code()
                user.activation_code_created_date = timezone.now()
                user.save()
        return render(request ,self.template_name)

class ForgotPassword(View):
    template_name = 'account_module/extends/_forgot_password.html'
    form_class = ResetPasswordForm

    def get(self, request):
        email = request.GET.get('email' or None)
        form = self.form_class(initial={'email':email})
        context = {'form' : form}
        return render(request, self.template_name , context)

@login_required
def log_out_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect(reverse("account_module:sign_in"))