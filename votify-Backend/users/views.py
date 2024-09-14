from .helpers.emails import reset_password, send_password_reset_confirmation_email
from .forms import PasswordResetRequestForm, SetNewPasswordForm
from .models import User, PasswordResetToken
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
    user = getattr(request, 'user', None)

    if user and user.is_authenticated and user.is_staff:
        context['admin_dashboard'] = True
    else:
        context['student_dashboard'] = True

    return render(request, '404.html', context, status=404)


def custom_500(request):
    context = {}
    user = getattr(request, 'user', None)

    if user and user.is_authenticated and user.is_staff:
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
        # Check if a file is uploaded
        uploaded_file = self.request.FILES.get('profile_pic')
        if uploaded_file:
            print("Uploaded file:", uploaded_file)

        # Save the form and provide success message
        response = super().form_valid(form)
        messages.success(
            self.request, 'Your profile has been updated successfully!')
        logger.info(
            f"User {self.request.user.email} successfully updated their profile.")
        return response

    def form_invalid(self, form):
        # Provide error message and log the issue
        messages.error(
            self.request, 'Error updating your profile. Please try again.')
        logger.warning(f"User {self.request.user.email} encountered an error while updating their profile.")
        return super().form_invalid(form)

# Reset Passwordfrom django.shortcuts import render, redirect


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            try:
                user = User.objects.get(email=email)
                # Create or refresh token
                token, created = PasswordResetToken.objects.get_or_create(
                    user=user)
                token.token = token.generate_token()  # Custom token generator
                token.is_used = False  # Reset the token usage
                token.save()

                # Generate the reset link
                reset_link = request.build_absolute_uri(
                    f"/user/reset-password/{urlsafe_base64_encode(force_bytes(user.pk))}/{token.token}/")
                # Print the URL for debugging
                print(f"Generated reset link: {reset_link}")
                # Prepare the email
                subject = "Password Reset Request"
                body = render_to_string('emails/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })

                # Send the reset email
                # Assuming this function sends email
                reset_password(email, subject, body)
                
                return redirect('password_reset_done')

                
            except User.DoesNotExist:
                messages.error(
                    request, 'No user with this email address found.')
            except Exception as e:
                print(f"Exception: {e}")

                messages.error(
                    request, 'Error occurred while sending the email. Please try again later.')
            return redirect('password_reset_request')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'pass/password_reset_request.html', {'form': form})


def password_reset(request, uidb64, token):
    print(f"Received UID: {uidb64}")
    print(f"Received Token: {token}")
    try:
        # Decode user ID from URL and get the user object
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(f"Decoded UID: {uid}")  # Debug statement

        user = User.objects.get(pk=uid)

        # Retrieve and validate the token
        token_obj = PasswordResetToken.objects.get(user=user, token=token, is_used=False)


        # Check if the token is expired
        if token_obj.is_expired():
            messages.error(request, 'The reset link has expired.')
            return redirect('password_reset_request')

    except (User.DoesNotExist, PasswordResetToken.DoesNotExist):
        messages.error(request, 'Invalid reset link or token.')
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = SetNewPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            token_obj.is_used = True  # Mark the token as used
            token_obj.save()
            
            # Send confirmation email
            subject = "Password Reset Successful"
            body = render_to_string('emails/password_reset_email_complete.html', {
                'user': user,
                'fullname': user.full_name,
            })
            send_password_reset_confirmation_email(user.email, subject, body)

            return redirect('password_reset_complete')
    else:
        form = SetNewPasswordForm(user=user)

    return render(request, 'pass/password_reset.html', {'form': form})


def password_reset_done(request):
    return render(request, 'pass/password_reset_done.html')


def password_reset_complete(request):
    return render(request, 'pass/password_reset_complete.html')


def password_reset_error(request):
    return render(request, 'pass/password_reset_error.html')
