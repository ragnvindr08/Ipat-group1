from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *
from django import forms
from django.forms import modelformset_factory
from .models import AttendanceRecord
from django.forms import BaseFormSet
from django.forms import BaseModelFormSet
from django.forms.renderers import get_default_renderer

class ReadOnlyField(forms.CharField):
    widget = forms.TextInput(attrs={'readonly': 'readonly'})

    def clean(self, value):
        return value

class OfficialTimeForm(forms.ModelForm):
    class Meta:
        model = OfficialTime
        fields = ['day','official_office_in', 'official_office_out', 'official_honorarium_time_in', 'official_honorarium_time_out', 'official_servicecredit_time_in', 'official_servicecredit_time_out', 'official_overtime_time_in', 'official_overtime_time_out']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day'].widget.attrs['readonly'] = True

# class CustomOfficialTimeFormSet(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         queryset = kwargs.pop('queryset', None)
#         super().__init__(*args, **kwargs)
#         for form in self.forms:
#             form.fields['employee_id'].widget.attrs['readonly'] = True
#             form.fields['day'].widget.attrs['readonly'] = True
#         self.queryset = queryset

#     model = OfficialTime
#     form = OfficialTimeForm
#     fields = '__all__'
#     extra = 0
#     min_num = 0
#     max_num = 0
#     renderer = get_default_renderer()
#     can_order = False  # Add this line to set can_order to False
# # class SearchForm(forms.Form):
# #     employee_id = forms.CharField(max_length=100)
# #     start_date = forms.DateField()
# #     end_date = forms.DateField()

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
    def __init__(self, *args, **kwargs):
        super(AttendanceRecordForm, self).__init__(*args, **kwargs)
        # Disable employee_id and date fields
        self.fields['employee_id'].disabled = True
        self.fields['date'].disabled = True

    class Meta:
        model = AttendanceRecord
        fields = ['employee_id', 'date', 'time_in', 'break_in', 'break_out', 'time_out', 'surplusHour_time_in', 'surplusHour_time_out']