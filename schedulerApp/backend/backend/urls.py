"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from scheduler import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'appointments', views.AppointmentView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include('user_api.urls')),
    path('api/appointments/', views.create_appointment, name='create_appointment')
]