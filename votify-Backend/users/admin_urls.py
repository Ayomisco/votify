from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from .views import AdminLoginView, CustomAdminSignupView

urlpatterns = [
    # Custom admin login page
    path('logout/', LogoutView.as_view(next_page='admin_login'),
         name='admin_logout'),  # Default Django logout
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('', admin.site.urls),

]
