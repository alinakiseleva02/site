from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('specializations/', views.specializations, name='specializations'),
    path('specialization/<int:specialization_id>/', views.doctors_by_specialization, name='doctors_by_specialization'),
    path('doctor/<int:doctor_id>/schedule/', views.schedule, name='schedule'),
    path('schedule/<int:schedule_id>/book/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:appointment_id>/confirmation/', views.appointment_confirmation, name='appointment_confirmation'),
]