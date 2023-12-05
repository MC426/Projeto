from django.urls import path
from . import views

urlpatterns = [
    path('create', views.AppointmentCreateView.as_view(), name='create'),
    path('list', views.AppointmentListView.as_view(), name = 'list'),
    path('list-in-period', views.ApointmentListInAPeriodView.as_view(), name = 'list-in-period'),
    path('create-room', views.RoomCreateView.as_view(), name='create-room'),
]