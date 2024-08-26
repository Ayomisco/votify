from .forms import CustomUserCreationForm, CustomAdminCreationForm, CustomLoginForm, AdminLoginForm
from .models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView 
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'Registration successful. Please log in.')
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, 'Registration failed. Please correct the errors below.')
        print(form.errors)

        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Login successful!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid matriculation number or password')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('dashboard')


def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:

                    # Ensure the user is an admin
                    if user.check_password(password) and users.is_staff:
                        login(request, user)
                        # Redirect to the admin dashboard
                        return redirect('admin:index')
                    else:
                        form.add_error(
                            None, "You do not have permission to access the admin.")
            form.add_error(None, "Invalid email or password.")

        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AdminLoginForm()

    return render(request, 'users/admin_login.html', {'form': form})


class CustomAdminSignupView(CreateView):
    form_class = CustomAdminCreationForm
    template_name = 'users/admin_signup.html'
    success_url = reverse_lazy('admin_login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True  # Make the user an admin
        user.is_superuser = True  # Ensure the user is not a superuser
        user.save()

        # Assign specific permissions
        content_type = ContentType.objects.get_for_model(User)
        permission_view_dashboard = Permission.objects.get(
            codename='can_view_dashboard', content_type=content_type)
        permission_manage_users = Permission.objects.get(
            codename='can_manage_users', content_type=content_type)
        permission_edit_users = Permission.objects.get(
            codename='can_edit_users', content_type=content_type)
        permission_delete_users = Permission.objects.get(
            codename='can_delete_users', content_type=content_type)

        user.user_permissions.add(
            permission_view_dashboard,
            permission_manage_users,
            permission_edit_users,
            permission_delete_users
        )

        messages.success(self.request, "Admin account created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Print form errors for debugging
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
