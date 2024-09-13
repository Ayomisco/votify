from django.urls import path
from .views import UserRegistrationView, CustomLoginView, IndexView,  CustomAdminSignupView, ProfileView, EditProfileView
from django.contrib.auth.views import LogoutView



urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_signup/', CustomAdminSignupView.as_view(), name='admin_signup'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
]
