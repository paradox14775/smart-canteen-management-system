from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, LoginForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_student_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Smart Canteen, {user.first_name}!")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been safely logged out.")
    return redirect('accounts:login')


@login_required
def dashboard_redirect_view(request):
    """
    Central dispatcher: routes user to their appropriate role portal.
    """
    user = request.user
    if user.is_superuser or user.role == User.Role.ADMIN:
        return redirect('orders:admin_dashboard')
    elif user.role == User.Role.KITCHEN:
        return redirect('orders:kds_board')
    elif user.role == User.Role.MANAGEMENT:
        return redirect('analytics:dashboard')
    else:
        return redirect('menu:customer_menu')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })
