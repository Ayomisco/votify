from django.urls import path
from .views import UserRegistrationView, CustomLoginView, IndexView,  CustomAdminSignupView, ProfileView, EditProfileView
from django.contrib.auth.views import LogoutView

from django.conf.urls import handler404, handler500
from .views import custom_404, custom_500

handler404 = custom_404
handler500 = custom_500

urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_signup/', CustomAdminSignupView.as_view(), name='admin_signup'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
]
