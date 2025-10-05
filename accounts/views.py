from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

from nursing.forms import UserRegistrationForm  # Your custom registration form
from nursing.models import UserProfile, Patient  # Your Profile model


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Check user role and redirect accordingly
            user_profile = getattr(user, 'userprofile', None)
            if user_profile:
                if user_profile.role == 'patient':
                    return redirect('dashboard')  # patient dashboard
                elif user_profile.role == 'doctor':
                    return redirect('doctor-dashboard')
                elif user_profile.role == 'nurse':
                    return redirect('nurse-dashboard')
                elif user_profile.role == 'receptionist':
                    return redirect('receptionist-dashboard')
            return redirect('/')  # fallback
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }



def signUp(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            if role == 'patient':
                # Create Patient record for this user
                Patient.objects.create(
                    first_name=user.first_name or user.username,
                    last_name=user.last_name or '',
                    email=user.email,
                    # Add other required fields as needed
                )
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'registration/register.html', context)


@login_required
def profile(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Profile'
    }
    return render(request, 'profile/profile.html', context)
