
from django.urls import path
from djangoauthapi_app.views import (SendPasswordResetEmailView, UserChangePasswordView,
       UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView)

urlpatterns = [
       path('register/', UserRegistrationView.as_view(), name='register'),
   
       path('login/', UserLoginView.as_view(), name='login'),

       path('profile/', UserProfileView.as_view(), name='profile'),

       path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),

       path('send_reset_pws_email/', SendPasswordResetEmailView.as_view(), name='send_reset_pws_email'),

       path('reset_password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password')

   
]
