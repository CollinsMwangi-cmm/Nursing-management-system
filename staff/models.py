from django.db import models
from django.contrib.auth.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()

class PatientRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='records')
    date = models.DateField(auto_now_add=True)
    diagnosis = models.CharField(max_length=255)
    treatment = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.date}"
    
    
class NurseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    

    def __str__(self):
        return self.user.get_full_name()


class Shift(models.Model):
    nurse = models.ForeignKey(NurseProfile, on_delete=models.CASCADE, related_name='shifts')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ward = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.nurse.user.get_full_name()} ({self.start_time} - {self.end_time})"


class NurseTask(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} for {self.shift.nurse.user.get_full_name()}"