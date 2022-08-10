from django.urls import path
from user_account.views import *
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('kayit-ol', RegistrationView.as_view(), name='register'),
    path('giris-yap', Login.as_view(), name='login'),
    path('cikis-yap', LogoutView.as_view(next_page='mainpage'), name='logout'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
]
