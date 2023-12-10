from django.urls import path
from . import views

urlpatterns = [
    path('create-appointment', views.AppointmentCreateView.as_view(), name='create-appointment'),
    path('list', views.AppointmentListView.as_view(), name = 'list'),
    path('list-in-period', views.AppointmentListInAPeriodView.as_view(), name = 'list-in-period'),
    path('manage-rooms', views.RoomManageView.as_view(), name='manage-rooms'),
    path('manage-room-reservations', views.RoomReservationManageView.as_view(), name='manage-room-reservations'),
    path('reserve-appointment',views.AppointmentReservation.as_view(), name='reserve-appointment'),
]