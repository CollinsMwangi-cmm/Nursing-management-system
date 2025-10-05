from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment, MedicalRecord, UserProfile, Notification
from django.contrib.auth.models import User
from .forms import AppointmentForm
from django.contrib import messages

def home(request):
    return render(request, 'base.html', {'title': 'Home'})


  
@login_required
def patient_dashboard(request):
    # Just a welcome, or quick stats if you want
    patient = None
    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'patient':
        try:
            patient = Patient.objects.get(email=request.user.email)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'dashboard.html', {'patient': patient})

@login_required
def book_appointment(request):
    patient = None
    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'patient':
        try:
            patient = Patient.objects.get(email=request.user.email)
        except Patient.DoesNotExist:
            patient = None
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if patient:
                appointment.patient = patient
                appointment.save()
                messages.success(request, "Appointment booked successfully!")
                return redirect('patient-appointments')
            else:
                messages.error(request, "Patient record not found.")
                return redirect('dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form, 'patient': patient})

@login_required
def patient_appointments(request):
    patient = None
    appointments = []
    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'patient':
        try:
            patient = Patient.objects.get(email=request.user.email)
            appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'patient_appointments.html', {'appointments': appointments, 'patient': patient})

@login_required
def patient_medications(request):
    patient = None
    medications = []
    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'patient':
        try:
            patient = Patient.objects.get(email=request.user.email)
            medications = Medication.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'patient_medications.html', {'medications': medications, 'patient': patient})

@login_required
def patient_reports(request):
    patient = None
    reports = []
    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'patient':
        try:
            patient = Patient.objects.get(email=request.user.email)
            reports = MedicalRecord.objects.filter(patient=patient).order_by('-record_date')
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'patient_reports.html', {'reports': reports, 'patient': patient})
    
@login_required
def doctor_dashboard(request):
    doctor = request.user
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    # You can also fetch patients or reports if needed
    return render(request, 'doctor_dashboard.html', {
        'appointments': appointments,
        # add patients/reports as needed
    })

@login_required
def nurse_dashboard(request):
    # Nurse-specific dashboard
    return render(request, 'nurse_dashboard.html')

@login_required
def receptionist_dashboard(request):
    # Receptionist-specific dashboard
    return render(request, 'receptionist_dashboard.html')