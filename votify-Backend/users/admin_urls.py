from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from .views import admin_login, CustomAdminSignupView

urlpatterns = [
    # Custom admin login page
    path('logout/', LogoutView.as_view(),
         name='admin_logout'),  # Default Django logout
    path('login/', admin_login, name='admin_login'),
    path('', admin.site.urls),

]
