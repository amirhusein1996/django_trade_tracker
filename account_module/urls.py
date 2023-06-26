from django.urls import path
from account_module.views import authorization , base

app_name ="account_module"

urlpatterns = [
    path('log-out/', authorization.log_out_view , name = "log_out"),
    path('sign-up/' , authorization.CreateAccount.as_view() , name='sign_up'),
    path('sign-in/' , authorization.Login.as_view() , name='sign_in'),
    path('register-message/' , authorization.SentEmailMessageTemplateView.as_view() , name="sent_email_message"),
    path('activation/<str:activate_code>' , authorization.ActiveUser.as_view() , name = 'active_user'),
    path('forgot-password/' , authorization.ForgotPassword.as_view() , name = "forgot_password"),



    path('edit-profile/', base.ProfileUpdateView.as_view() , name='edit_profile'),

]