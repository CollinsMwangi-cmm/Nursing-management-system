from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

from nursing.forms import UserRegistrationForm  # Your custom registration form
from nursing.models import UserProfile  # Your Profile model


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
            # Create UserProfile with additional fields from form
            UserProfile.objects.create(
                user=user,
                location=form.cleaned_data.get('location', ''),
                phone=form.cleaned_data.get('phone', ''),
                role=form.cleaned_data.get('role')
            )
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('challenge_list')  # Change to your desired redirect
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
