from django.urls import path
from . import views

urlpatterns = [
    path('create', views.AppointmentCreateView.as_view(), name='create'),
    path('list', views.AppointmentListView.as_view(), name = 'list')
]