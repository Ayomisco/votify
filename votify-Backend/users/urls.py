from django.urls import path
from .views import UserRegisterView, CustomLoginView, admin_login, CustomAdminSignupView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_signup/', CustomAdminSignupView.as_view(), name='admin_signup'),

]
