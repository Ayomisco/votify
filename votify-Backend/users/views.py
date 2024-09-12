from .forms import UserProfileForm  # Ensure you import the form
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.views import View
from django.contrib.auth.views import LoginView as DjangoLoginView
from .forms import CustomUserCreationForm, CustomLoginForm, AdminLoginForm, UserProfileForm,  CustomAdminCreationForm
from .models import User
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from elections.models import Election, Candidate, Vote
from results.models import Result, Winner
# Set up logging
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


def custom_404(request, exception=None):
    context = {}
    user = request.user

    if user.is_staff:
        context['admin_dashboard'] = True
    else:
        context['student_dashboard'] = True

    return render(request, '404.html', context, status=404)


def custom_500(request):
    context = {}
    user = request.user

    if user.is_staff:
        context['admin_dashboard'] = True
    else:
        context['student_dashboard'] = True

    return render(request, '500.html', context, status=500)

    

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch active elections
        active_elections = Election.objects.filter(status='Active')

        # Fetch winners
        election_winners = []

        for election in active_elections:
            # Get results and winners
            result = Result.objects.filter(election=election).first()
            if result:
                winners = Winner.objects.filter(result=result)
                for winner in winners:
                    candidate = winner.candidate
                    election_winners.append({
                        'name': candidate.full_name,
                        'email': candidate.email,
                        'image': candidate.image.url if candidate.image else None,
                        'election': election.election_type
                    })

        context['election_winners'] = election_winners
        context['active_elections'] = active_elections

        # Determine dashboard type based on user
        if user.is_staff:
            context['admin_dashboard'] = True
        else:
            context['student_dashboard'] = True

        return context

class UserRegistrationView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect if already authenticated
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

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




class CustomLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect if already authenticated
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

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


class AdminLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class AdminLoginView(View):
    def get(self, request):
        form = AdminLoginForm()
        return render(request, 'users/admin_login.html', {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect if already authenticated
            return redirect('admin:index')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None and user.is_staff:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('admin:index')
            else:
                messages.error(
                    request, 'Invalid email or password, or you do not have permission to access the admin.')
        # Optional: Add specific form validation error feedback
        else:    
            messages.error(request, 'Please correctly fill the form.')

        # Always re-render the form in the context if the login fails
        return render(request, 'users/admin_login.html', {'form': form})

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


class ProfileView(LoginRequiredMixin, TemplateView):
    """Displays the user's profile page with all you know information."""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = user.full_name
        context['email'] = user.email
        context['matriculation_number'] = user.matriculation_number
        context['department'] = user.department
        context['profile_pic'] = user.profile_pic
        context['form'] = UserProfileForm(instance=user)  # Add this line
        logger.info(f"User {user.email} viewed their profile.")
        return context



class EditProfileView(LoginRequiredMixin, UpdateView):
    """Allows users to edit their profile."""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request, 'Your profile has been updated successfully!')
        logger.info(
            f"User {self.request.user.email} successfully updated their profile.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Error updating your profile. Please try again.')
        logger.warning(f"User {self.request.user.email} encountered an error while updating their profile.")
        return super().form_invalid(form)
