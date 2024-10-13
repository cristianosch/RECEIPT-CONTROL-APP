from django.urls import path
from . import views
from .views import ResetPasswordView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('registration/', views.signUp, name= 'SignUp'),    
    path('profile/', views.profile, name= 'profile'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),       
]
