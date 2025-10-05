from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_dashboard, name='dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor-dashboard'),
    path('nurse/', views.nurse_dashboard, name='nurse-dashboard'),
    path('receptionist/', views.receptionist_dashboard, name='receptionist-dashboard'),
  
]