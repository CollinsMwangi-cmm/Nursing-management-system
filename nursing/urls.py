from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_dashboard, name='dashboard'),
    path('book-appointment/', views.book_appointment, name='book-appointment'),
    path('appointments/', views.patient_appointments, name='patient-appointments'),
    path('medications/', views.patient_medications, name='patient-medications'),
    path('reports/', views.patient_reports, name='patient-reports'),
    path('doctor/', views.doctor_dashboard, name='doctor-dashboard'),
    path('nurse/', views.nurse_dashboard, name='nurse-dashboard'),
    path('receptionist/', views.receptionist_dashboard, name='receptionist-dashboard'),
]