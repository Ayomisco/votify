from django.urls import path
from .views import UserRegistrationView, CustomLoginView, password_reset_request, password_reset, password_reset_done, password_reset_complete, password_reset_error,  CustomAdminSignupView, ProfileView, EditProfileView
from django.contrib.auth.views import LogoutView



urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_signup/', CustomAdminSignupView.as_view(), name='admin_signup'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('password-reset/', password_reset_request,
         name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/',
         password_reset, name='password_reset'),
    path('password-reset/done/', password_reset_done, name='password_reset_done'),
    path('password-reset/complete/', password_reset_complete,
         name='password_reset_complete'),
    path('password-reset/error/', password_reset_error,
         name='password_reset_error'),

]
