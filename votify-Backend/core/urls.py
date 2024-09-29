"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import IndexView, DashboardView
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls import handler404, handler500
from users.views import custom_404, custom_500

handler404 = 'users.views.custom_404'
handler500 = 'users.views.custom_500'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('user/', include('users.urls')),

    
    

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('admin/', include('users.admin_urls')),  # Include custom admin URLs

    path('', include('elections.urls')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
