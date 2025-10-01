from django import forms
from django.contrib.auth.models import User
from .models import PatientProfile, PatientRecord, NurseProfile, Shift, NurseTask


class NurseProfileForm(forms.ModelForm):
    class Meta:
        model = NurseProfile
        fields = ['user', 'phone', 'department']

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['nurse', 'start_time', 'end_time', 'ward']

class NurseTaskForm(forms.ModelForm):
    class Meta:
        model = NurseTask
        fields = ['shift', 'description', 'completed']


class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['diagnosis', 'treatment', 'notes']

class PatientCreationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'phone', 'address']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email']
        )
        # Now create PatientProfile and link to User
        patient_profile = PatientProfile(
            user=user,
            date_of_birth=self.cleaned_data['date_of_birth'],
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address']
        )
        if commit:
            patient_profile.save()
        return patient_profile