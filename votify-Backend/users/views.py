# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.views import View
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomLoginForm, AdminLoginForm, CustomAdminCreationForm
from .models import User
from django.views.generic import TemplateView
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'index.html'

    

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UserRegistrationView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
            self.request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(
                self.request, 'Registration failed. Please correct the errors below.')
            print(form.errors)

        return render(request, 'users/register.html', {'form': form})


class CustomLoginView(DjangoLoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        matriculation_number = form.cleaned_data.get('matriculation_number')
        password = form.cleaned_data.get('password')
        user = authenticate(
            matriculation_number=matriculation_number, password=password)
        if user is not None:
            auth_login(self.request, user)
            messages.success(self.request, 'Login successful!')

            return redirect('dashboard')
        else:
            messages.error(
                self.request, 'Invalid matriculation number or password')
        return super().form_invalid(form)


class AdminLoginView(DjangoLoginView):
    template_name = 'users/admin_login.html'
    form_class = AdminLoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None and user.is_staff:
            auth_login(self.request, user)
            messages.success(self.request, 'Login successful!')

            return redirect('admin:index')
        else:
            messages.error(
                self.request, 'Invalid email or password.')
        return super().form_invalid(form)


class CustomAdminSignupView(View):
    def get(self, request):
        form = CustomAdminCreationForm()
        return render(request, 'users/admin_signup.html', {'form': form})

    def post(self, request):
        form = CustomAdminCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.is_staff = True  # Make the user an admin
            form.is_superuser = True  # Ensure the user is not a superuser
            form.save()
            messages.success(
                self.request, "Admin account created successfully.")

            return redirect('admin_login')
        return render(request, 'users/admin_signup.html', {'form': form})
