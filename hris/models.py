from django.db import models
from django.contrib.auth.models import User
from datetime import time
# Create your models here.



class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,unique=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="Default_pfp.jpg", null=True, blank=True)
    employee_id = models.CharField(max_length=20,unique=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    name_ext = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    civil_status = models.CharField(max_length=20, blank=True, null=True)
    height_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    gsis_no = models.CharField(max_length=20, blank=True, null=True)
    pagibig_no = models.CharField(max_length=20, blank=True, null=True)
    philhealth_no = models.CharField(max_length=20, blank=True, null=True)
    sss_no = models.CharField(max_length=20, blank=True, null=True)
    tin_no = models.CharField(max_length=20, blank=True, null=True)
    agency_em = models.CharField(max_length=100, blank=True, null=True)
    citizenship = models.CharField(max_length=50, blank=True, null=True)
    residential_house_no = models.CharField(max_length=10, blank=True, null=True)
    residential_street = models.CharField(max_length=100, blank=True, null=True)
    residential_subd = models.CharField(max_length=100, blank=True, null=True)
    residential_brgy = models.CharField(max_length=100, blank=True, null=True)
    residential_city = models.CharField(max_length=100, blank=True, null=True)
    residential_province = models.CharField(max_length=100, blank=True, null=True)
    residential_zipcode = models.CharField(max_length=10, blank=True, null=True)
    permanent_house_no = models.CharField(max_length=10, blank=True, null=True)
    permanent_street = models.CharField(max_length=100, blank=True, null=True)
    permanent_subd = models.CharField(max_length=100, blank=True, null=True)
    permanent_brgy = models.CharField(max_length=100, blank=True, null=True)
    permanent_city = models.CharField(max_length=100, blank=True, null=True)
    permanent_province = models.CharField(max_length=100, blank=True, null=True)
    permanent_zipcode = models.CharField(max_length=10, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    spouse_surname = models.CharField(max_length=100, blank=True, null=True)
    spouse_first_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_middle_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_name_ext = models.CharField(max_length=10, blank=True, null=True)
    spouse_occupation = models.CharField(max_length=100, blank=True, null=True)
    spouse_employer = models.CharField(max_length=100, blank=True, null=True)
    spouse_business_address = models.CharField(max_length=200, blank=True, null=True)
    spouse_telephone = models.CharField(max_length=20, blank=True, null=True)
    elementary_education = models.CharField(max_length=200, blank=True, null=True)
    secondary_education = models.CharField(max_length=200, blank=True, null=True)
    father_surname = models.CharField(max_length=100, blank=True, null=True)
    father_first_name = models.CharField(max_length=100, blank=True, null=True)
    father_middle_name = models.CharField(max_length=100, blank=True, null=True)
    father_name_ext = models.CharField(max_length=10, blank=True, null=True)
    mother_surname = models.CharField(max_length=100, blank=True, null=True)
    mother_first_name = models.CharField(max_length=100, blank=True, null=True)
    mother_middle_name = models.CharField(max_length=100, blank=True, null=True)
    employment_status = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    employment_status = models.DateTimeField(auto_now_add=True, null= True)
    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.surname}"


class OfficialTime(models.Model):
    employee_id = models.CharField(max_length=20)
    day = models.CharField(max_length = 10)
    semester_id = models.CharField(max_length = 10, null= True, blank = True)
    official_office_in = models.TimeField(null= True, blank = True)
    official_office_out = models.TimeField(null= True, blank = True)
    official_honorarium_time_in = models.TimeField(null= True, blank = True)
    official_honorarium_time_out = models.TimeField(null= True, blank = True)
    official_servicecredit_time_in = models.TimeField(null= True, blank = True)
    official_servicecredit_time_out = models.TimeField(null= True, blank = True)
    official_overtime_time_in = models.TimeField(null= True, blank = True)
    official_overtime_time_out = models.TimeField(null= True, blank = True)


class AttendanceRecord(models.Model):
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time_in = models.TimeField(default='00:00:00', null=True, blank=True)
    break_in = models.TimeField(default='00:00:00', null=True, blank=True)
    break_out = models.TimeField(default='00:00:00', null=True, blank=True)
    time_out = models.TimeField(default='00:00:00', null=True, blank=True)
    surplusHour_time_in = models.TimeField(default='00:00:00', null=True, blank=True)
    surplusHour_time_out = models.TimeField(default='00:00:00', null=True, blank=True)

    def __str__(self):
        return f"{self.employee_id} - {self.date}" if self.date else self.employee_id