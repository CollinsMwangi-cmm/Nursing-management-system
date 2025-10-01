from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PatientProfile, PatientRecord, Shift, NurseProfile, NurseTask
from .forms import PatientCreationForm, PatientRecordForm, NurseProfileForm, ShiftForm, NurseTaskForm
from django.contrib.auth.models import User

def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def list_nurses(request):
    nurses = NurseProfile.objects.select_related('user').all()
    return render(request, 'staff/list_nurses.html', {'nurses': nurses})

@login_required
@user_passes_test(is_staff)
def add_shift(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_shifts')
    else:
        form = ShiftForm()
    return render(request, 'staff/add_shift.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def list_shifts(request):
    shifts = Shift.objects.select_related('nurse__user').all().order_by('-start_time')
    return render(request, 'staff/list_shifts.html', {'shifts': shifts})

@login_required
@user_passes_test(is_staff)
def add_task(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    if request.method == 'POST':
        form = NurseTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.shift = shift
            task.save()
            return redirect('view_shift', shift_id=shift_id)
    else:
        form = NurseTaskForm(initial={'shift': shift})
    return render(request, 'staff/add_task.html', {'form': form, 'shift': shift})

@login_required
@user_passes_test(is_staff)
def view_shift(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    tasks = shift.tasks.all()
    return render(request, 'staff/view_shift.html', {'shift': shift, 'tasks': tasks})

@login_required
@user_passes_test(is_staff)
def add_patient_record(request, patient_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    if request.method == 'POST':
        form = PatientRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('view_patient_records', patient_id=patient_id)
    else:
        form = PatientRecordForm()
    return render(request, 'staff/add_patient_record.html', {'form': form, 'patient': patient})

@login_required
@user_passes_test(is_staff)
def view_patient_records(request, patient_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    records = patient.records.order_by('-date')
    return render(request, 'staff/view_patient_records.html', {'patient': patient, 'records': records})

@login_required
@user_passes_test(is_staff)
def list_patients(request):
    patients = PatientProfile.objects.select_related('user').all()
    return render(request, 'staff/list_patients.html', {'patients': patients})

@login_required
@user_passes_test(is_staff)
def add_patient(request):
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_patients')
    else:
        form = PatientCreationForm()
    return render(request, 'staff/add_patient.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def edit_patient(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk)
    user = patient.user
    if request.method == 'POST':
        form = PatientCreationForm(request.POST, instance=patient)
        if form.is_valid():
            # Update user fields manually
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            return redirect('list_patients')
    else:
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
        }
        form = PatientCreationForm(instance=patient, initial=initial)
    return render(request, 'staff/edit_patient.html', {'form': form, 'patient': patient})

@login_required
@user_passes_test(is_staff)
def delete_patient(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk)
    if request.method == 'POST':
        user = patient.user
        patient.delete()
        user.delete()
        return redirect('list_patients')
    return render(request, 'staff/delete_patient.html', {'patient': patient})

@login_required
@user_passes_test(is_staff)
def patient_detail(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk)
    return render(request, 'staff/patient_detail.html', {'patient': patient})

@login_required
@user_passes_test(is_staff)
def edit_patient_record(request, patient_id, record_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    record = get_object_or_404(PatientRecord, pk=record_id, patient=patient)
    if request.method == 'POST':
        form = PatientRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('view_patient_records', patient_id=patient_id)
    else:
        form = PatientRecordForm(instance=record)
    return render(request, 'staff/edit_patient_record.html', {'form': form, 'patient': patient, 'record': record})

@login_required
@user_passes_test(is_staff)
def delete_patient_record(request, patient_id, record_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    record = get_object_or_404(PatientRecord, pk=record_id, patient=patient)
    if request.method == 'POST':
        record.delete()
        return redirect('view_patient_records', patient_id=patient_id)
    return render(request, 'staff/delete_patient_records.html', {'patient': patient, 'record': record})