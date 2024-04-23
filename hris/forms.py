from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *
from django import forms
from django.forms import modelformset_factory
from .models import AttendanceRecord

# class SearchForm(forms.Form):
#     employee_id = forms.CharField(max_length=100)
#     start_date = forms.DateField()
#     end_date = forms.DateField()

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['employee_id', 'date', 'time_in', 'break_in', 'break_out', 'time_out', 'surplusHour_time_in', 'surplusHour_time_out']

AttendanceRecordFormSet = modelformset_factory(AttendanceRecord, form=AttendanceRecordForm, extra=0)


class SearchForm(forms.Form):
    employee_id = forms.CharField(label='Employee ID', max_length=100)
    start_date = forms.DateField(label='Start Date', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    end_date = forms.DateField(label='End Date', widget=forms.TextInput(attrs={'autocomplete': 'off'}))



class SearchAttendance(forms.Form):
    employee_id = forms.CharField(label='Employee ID', max_length=100)
    start_date = forms.DateField(label='Start Date', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    end_date = forms.DateField(label='End Date', widget=forms.TextInput(attrs={'autocomplete': 'off'}))


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username','email', 'password1', 'password2']
        
        
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user','employee_id']
        
        
class UploadFileForm(forms.Form):
    file = forms.FileField()

class FileUploadForm(forms.Form):
    file = forms.FileField()


class AttendanceSearchForm(forms.Form):
    employee_id = forms.CharField(max_length=100, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['employee_id', 'date', 'time_in', 'break_in', 'break_out', 'time_out', 'surplusHour_time_in', 'surplusHour_time_out']