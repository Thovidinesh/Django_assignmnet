# main_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse

# Login view using Django's AuthenticationForm
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # If form is valid, authenticate and log in the user
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            # If form is invalid, show error messages
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = AuthenticationForm()

    return render(request, 'main_app/login.html', {'form': form})

# Signup view using Django's UserCreationForm
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # If form is valid, save the user and show success message
            form.save()
            messages.success(request, 'Signup successful. You can now log in.')
            return redirect('login')
        else:
            # If form is invalid, show error messages
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()

    return render(request, 'main_app/signup.html', {'form': form})

# Forgot Password view using Django's PasswordResetForm
def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)  # Sends password reset email
            messages.success(request, 'Password reset instructions sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'Please enter a valid email address.')
    else:
        form = PasswordResetForm()

    return render(request, 'main_app/forgot_password.html', {'form': form})

# Change Password view using Django's PasswordChangeForm
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # If the form is valid, save the new password and update session
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after changing password
            messages.success(request, 'Your password has been updated!')
            return redirect('dashboard')
        else:
            # If form is invalid, show error messages
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'main_app/change_password.html', {'form': form})

# Dashboard view (Requires Authentication)
@login_required
def dashboard_view(request):
    return render(request, 'main_app/dashboard.html', {'username': request.user.username})

# Profile view (Requires Authentication)
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'main_app/profile.html', {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    })

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
