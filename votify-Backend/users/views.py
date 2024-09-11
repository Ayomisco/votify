import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.views import View
from django.contrib.auth.views import LoginView as DjangoLoginView
from .forms import CustomUserCreationForm, CustomLoginForm, AdminLoginForm, CustomAdminCreationForm
from .models import User
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Set up logging
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_staff:
            context['admin_dashboard'] = True  # Admin-specific data
        else:
            context['student_dashboard'] = True  # Student-specific data
        return context


class UserRegistrationView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        logger.debug(f"Form data: {request.POST}")

        try:
            if form.is_valid():
                form.save()
                messages.success(
                    self.request, 'Registration successful. Please log in.')
                return redirect('dashboard')
            else:
                messages.error(
                    self.request, 'Registration failed. Please correct the errors below.')
                logger.error(f"Form errors: {form.errors}")
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {e}")
            messages.error(
                self.request, 'An unexpected error occurred. Please try again later.')

        return render(request, 'users/register.html', {'form': form})


'''
class CustomLoginView(DjangoLoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        matriculation_number = form.cleaned_data.get('matriculation_number')
        password = form.cleaned_data.get('password')
        try:
            user = authenticate(
                matriculation_number=matriculation_number, password=password)
            if user is not None:
                auth_login(self.request, user)
                messages.success(self.request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(
                    self.request, 'Invalid matriculation number or password')
                logger.warning(f"Login failed for matriculation number: {matriculation_number}")
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            messages.error(
                self.request, 'An unexpected error occurred. Please try again later.')
            return self.form_invalid(form)

        

    def post(self, request, *args, **kwargs):
        logger.debug(f"POST data: {request.POST}")
        return super().post(request, *args, **kwargs)'''


class CustomLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        # Extract form data
        matriculation_number = request.POST.get('matriculation_number')
        password = request.POST.get('password')

        logger.debug(f"Attempting login with matriculation number: {matriculation_number}")

        try:
            # Authenticate user
            user = authenticate(
                request, matriculation_number=matriculation_number, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                logger.info(f"Login successful for matriculation number: {matriculation_number}")
                return redirect('dashboard')
            else:
                messages.error(
                    request, 'Invalid matriculation number or password.')
                logger.warning(f"Login failed for matriculation number: { matriculation_number}")
                return render(request, 'users/login.html')
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            messages.error(
                request, 'An unexpected error occurred. Please try again later.')
            return render(request, 'users/login.html')


class AdminLoginView(View):
    def get(self, request):
        return render(request, 'users/admin_login.html')

    def post(self, request):
        # Extract form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        logger.debug(f"Attempting admin login with email: {email}")

        try:
            # Authenticate user
            user = authenticate(request, username=email, password=password)

            if user is not None and user.is_staff:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                logger.info(f"Admin login successful for email: {email}")
                return redirect('admin:index')
            else:
                messages.error(
                    request, 'Invalid email or password, or you do not have permission to access the admin.')
                logger.warning(f"Admin login failed for email: {email}")
                return render(request, 'users/admin_login.html')
        except Exception as e:
            logger.error(f"Unexpected error during admin login: {e}")
            messages.error(
                request, 'An unexpected error occurred. Please try again later.')
            return render(request, 'users/admin_login.html')


class CustomAdminSignupView(View):
    def get(self, request):
        form = CustomAdminCreationForm()
        return render(request, 'users/admin_signup.html', {'form': form})

    def post(self, request):
        form = CustomAdminCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True  # Make the user an admin
                user.is_superuser = True  # Ensure the user is a superuser
                user.save()
                messages.success(
                    self.request, "Admin account created successfully.")
                return redirect('admin_login')
            else:
                messages.error(
                    self.request, 'Admin account creation failed. Please correct the errors below.')
                logger.error(f"Admin signup form errors: {form.errors}")
        except Exception as e:
            logger.error(f"Unexpected error during admin signup: {e}")
            messages.error(
                self.request, 'An unexpected error occurred. Please try again later.')

        return render(request, 'users/admin_signup.html', {'form': form})
