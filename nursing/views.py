from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment, MedicalRecord, UserProfile
from django.contrib.auth.models import User
from .forms import AppointmentForm
from django.contrib import messages

def home(request):
    return render(request, 'base.html', {'title': 'Home'})


  
@login_required
def patient_dashboard(request):
    patient = None
    appointments = []
    reports = []
    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'patient':
        try:
            patient = Patient.objects.get(email=request.user.email)
            appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
            reports = MedicalRecord.objects.filter(patient=patient).order_by('-record_date')
        except Patient.DoesNotExist:
            patient = None

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if patient is not None:
                appointment.patient = patient  # THIS IS REQUIRED!
                appointment.save()
                return redirect('dashboard')
            else:
                # Patient record not found; handle error
                messages.error(request, "Patient record not found. Please contact admin.")
                return redirect('dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'reports': reports,
        'form': form,
    })
    
@login_required
def doctor_dashboard(request):
    # Doctor-specific dashboard
    return render(request, 'doctor_dashboard.html')

@login_required
def nurse_dashboard(request):
    # Nurse-specific dashboard
    return render(request, 'nurse_dashboard.html')

@login_required
def receptionist_dashboard(request):
    # Receptionist-specific dashboard
    return render(request, 'receptionist_dashboard.html')