from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment, MedicalRecord, UserProfile
from django.contrib.auth.models import User
from .forms import AppointmentForm

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
            pass

    # Appointment booking logic
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            return redirect('patient-dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'reports': reports,
        'form': form,
    })