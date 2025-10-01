from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.list_patients, name='list_patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<int:pk>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:pk>/delete/', views.delete_patient, name='delete_patient'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/records/add/', views.add_patient_record, name='add_patient_record'),
    path('patients/<int:patient_id>/records/', views.view_patient_records, name='view_patient_records'),
    path('patients/<int:patient_id>/records/<int:record_id>/edit/', views.edit_patient_record, name='edit_patient_record'),
    path('patients/<int:patient_id>/records/<int:record_id>/delete/', views.delete_patient_record, name='delete_patient_record'),
    path('nurses/', views.list_nurses, name='list_nurses'),
    path('shifts/', views.list_shifts, name='list_shifts'),
    path('shifts/add/', views.add_shift, name='add_shift'),
    path('shifts/<int:shift_id>/', views.view_shift, name='view_shift'),
    path('shifts/<int:shift_id>/tasks/add/', views.add_task, name='add_task'),
]