from django.db import models
from django.contrib.auth.models import User

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
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.surname}"
    
    # class OfficialTIme(models.Model):
    #     CATEGORY = (
    #             ('Regular', 'Regul2ar'),
    #             ('Job Order','Job Order'),
    #             ('Job Order','Job Order'),
    #             )
    #     name = models.CharField(max_length = 200, null= True)
    #     price = models.FloatField(null=True)
    #     category = models.CharField(max_length = 200, null= True, choices = CATEGORY)
    #     description = models.CharField(max_length = 200, null= True, blank = True)
    #     date_created = models.DateTimeField(auto_now_add=True, null= True)
    
    # def __str__(self):
    #     return self.name
    
    
    # class Order(models.Model):
    #     STATUS = (
    #             ('Pending', 'Pending'),
    #             ('Out for Delivery','Out for Delivery'),
    #             ('Delivered', 'Delivered'),
    #             )

    #     customer = models.ForeignKey(Employee, null=True, on_delete= models.SET_NULL)
    #     product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    #     date_created = models.DateTimeField(auto_now_add=True, null= True)
    #     status = models.CharField(max_length = 200, null=True, choices=STATUS)
    #     note = models.CharField(max_length = 1000, null=True)
        
    #     def __str__(self):
    #         return self.product.name

    
class OfficialTime(models.Model):
    employee_id = models.CharField(max_length=20)
    day = models.CharField(max_length = 10)
    semester_id = models.CharField(max_length = 10, null= True, blank = True)
    office_time_start = models.TimeField(null= True, blank = True)
    office_time_end = models.TimeField(null= True, blank = True)
    honorarium_time_start = models.TimeField(null= True, blank = True)
    honorarium_time_end = models.TimeField(null= True, blank = True)
    servicecredit_time_start = models.TimeField(null= True, blank = True)
    servicecredit_time_end = models.TimeField(null= True, blank = True)
    overtime_time_start = models.TimeField(null= True, blank = True)
    overtime_time_end = models.TimeField(null= True, blank = True)


# class DTR(models.Model):
#     employee_id = models.CharField(max_length=20)
#     date = models.DateTimeField(auto_now_add=True)
#     ipAddress = models.IPAddressField()    
