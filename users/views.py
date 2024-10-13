from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from .forms import EditProfile
from django.contrib.messages import constants
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin



def signUp(request):
    if request.method == 'POST':
        fm = UserCreationForm(request.POST) 
        if fm.is_valid():
            fm.save()
        return redirect('dashboard')
    else:
        fm = UserCreationForm()
    return render(request, 'accounts/registration.html', {'form':fm})


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edited successfully')           
            return redirect('profile') 
    else:
        form = EditProfile(instance=profile)
        
    return render(request, 'accounts/profile.html', {
        'form':form,
        'profile' : profile
        })


class PasswordResetConfirmView(PasswordResetConfirmView):
   template_name = 'registration/password_reset_confirm/password_reset_confirm.html'
   success_url = reverse_lazy("users:password_reset_complete")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')


class PasswordResetCompleteView(PasswordResetCompleteView):
   template_name = 'registration/password_reset_confirm/password_reset_complete.html'
   success_url = reverse_lazy('login')