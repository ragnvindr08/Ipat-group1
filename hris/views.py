from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .decorators import *
from .signals import *
import datetime


#upload imports
import csv
import xlrd
from django.shortcuts import render
from django.shortcuts import get_object_or_404




from django.conf import settings
import os
# Create your views here.

#UPLOAD DTR .DAT FILE
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Read and process each line in the uploaded file
            for line in uploaded_file:
                line = line.decode('utf-8').strip()  # Decode bytes to string and remove leading/trailing whitespace
                if line:  # Check if line is not empty
                    columns = line.split('\t')  # Split each line into columns based on tab delimiter

                    # Ensure that columns list has at least 2 elements before processing
                    if len(columns) >= 2:
                        employee_number = int(columns[0]) if columns[0].strip() else None

                        # Extract only the date part from columns[1]
                        date_time_parts = columns[1].split()
                        date_only = None
                        if len(date_time_parts) > 0:
                            date_only = date_time_parts[0]  # Extract only the date part

                        # Extracting other columns
                        if len(columns) >= 6:
                            column1 = int(columns[2])
                            column2 = int(columns[3])
                            column3 = int(columns[4])
                            column4 = int(columns[5])

                        # Check if an AttendanceRecord already exists for the employee and date
                        existing_records = AttendanceRecord.objects.filter(employee_id=employee_number, date=date_only)

                        # Create a new AttendanceRecord instance if it doesn't exist
                        if existing_records.exists():
                            record = existing_records.first()
                        else:
                            record = AttendanceRecord(employee_id=employee_number, date=date_only)

                        # Assigning time components to the appropriate fields based on column values
                        # Note: I assume you want to save the full date_time string for time-related fields
                        if columns[1]:  # Check if date_time is not empty
                            if column1 == 1 and column2 == 0 and column3 == 1 and column4 == 0:
                                
                                    record.time_in = columns[1]
                            elif column1 == 1 and column2 == 1 and column3 == 1 and column4 == 0:
                                record.break_in = columns[1]
                            elif column1 == 1 and column2 == 4 and column3 == 1 and column4 == 0:
                                record.break_out = columns[1]
                            elif column1 == 1 and column2 == 5 and column3 == 1 and column4 == 0:
                                record.time_out = columns[1]
                            elif column1 == 1 and column2 == 4 and column3 == 0 and column4 == 0:
                                if not record.time_in:
                                    record.time_in = columns[1]
                                else:
                                    record.surplusHour_time_in = columns[1]
                                   
                            elif column1 == 1 and column2 == 5 and column3 == 0 and column4 == 0:
                                if not record.time_out:
                                    record.time_out = columns[1]
                                else:
                                    record.surplusHour_time_out = columns[1]

                        record.save()  # Save the record to the database

            return render(request, 'hris/upload_success.html')
    else:
        form = FileUploadForm()
    return render(request, 'hris/upload2.html', {'form': form})


def upload_success(request):
    return render(request, 'hris/upload_success.html')
#UPLOAD DTR END


@login_required(login_url='login')
@admin_only
def registerPage(request):
    if request.user.is_authenticated:

        form = CreateUserForm()
        groups = Group.objects.all()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get('username')

                group_name = request.POST.get('group')
                if group_name:
                    group = Group.objects.get(name=group_name)
                    user.save()
                    user.groups.add(group)

                employee_number = request.POST.get('employee_number')
                 # Create OfficialTime records for each day of the week
                days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                for day in days_of_week:
                    OfficialTime.objects.create(
                            employee_id=employee_number,
                            day=day
                        )
                try:
                    # Try to retrieve existing employee profile for the user
                    employee_profile = Employee.objects.get(user=user)
                    # Update existing employee profile with new employee number
                    employee_profile.employee_id = employee_number
                    employee_profile.save()
                except Employee.DoesNotExist:
                    # Create new employee profile if it doesn't exist
                    employee_profile = Employee.objects.create(
                        user=user,
                        employee_id=employee_number,
                        first_name=user.first_name,
                        surname=user.last_name
                    )

                   

                messages.success(request, 'Account was created for ' + username)
                return redirect('register')

        context = {'form': form, 'groups': groups}
        return render(request, 'hris/register.html', context)
       
    else:   
         return redirect('home')
    
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username and password is incorrect')

    context = {}
    return render(request, 'hris/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
@admin_only
def home(request):
    # # orders = Order.objects.all()
    # customers = Employee.objects.all()
    # profile = request.user.customer
    # total_customers = customers.count()
    # total_orders = orders.count()
    # delivered = orders.filter(status='Delivered').count()
    # pending = orders.filter(status='Pending').count()
    
    # context = {'orders':orders, 'customers':customers, 
    # 'total_orders':total_orders, 'delivered': delivered,
    # 'pending': pending }
    
    return render(request, 'hris/home.html',)



def accountSettings(request):
    employee = request.user.employee
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            # Save form data
            form.save()

            # Rename the profile picture if it exists
            if 'profile_pic' in request.FILES:
                # Get the uploaded profile picture
                profile_picture = request.FILES['profile_pic']

                # Rename the profile picture file using the username
                username = request.user.username
                file_name, file_extension = os.path.splitext(profile_picture.name)
                new_file_name = f"{username}{file_extension}"

                # Construct the correct file path
                file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)

                # Rename the file in the filesystem
                with open(file_path, 'wb+') as destination:
                    for chunk in profile_picture.chunks():
                        destination.write(chunk)

                # Update the profile picture name in the customer object
                employee.profile_pic.name = new_file_name
                employee.save()

    context = {'form': form}
    return render(request, 'hris/account_settings.html', context)


# @login_required(login_url='login')
def userPage(request):
    pass


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                data = csv.reader(file)
            elif file.name.endswith('.xlsx'):
                data = xlrd.open_workbook(file_contents=file.read())
            else:
                messages.error(request, 'Unsupported file format')
                return redirect('upload_file')

            for row in data:
                employee_id, ip_address = row[0], row[1]
                DTR.objects.create(employee_id=employee_id, ip_address=ip_address)
            
            messages.success(request, 'Data has been successfully uploaded.')
            return redirect('upload_file')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


# def search_records(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             employee_id = form.cleaned_data['employee_id']
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             records = AttendanceRecord.objects.filter(employee_id=employee_id, date__range=(start_date, end_date))
#             return render(request, 'hris/records.html', {'records': records})
#     else:
#         form = SearchForm()
#     return render(request, 'hris/search.html', {'form': form})
def search_records(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Query the Employee model to get additional information about the employee
            employee = get_object_or_404(Employee, employee_id=employee_id)

            # Query the AttendanceRecord model to fetch records for the employee within the date range
            records = AttendanceRecord.objects.filter(employee_id=employee_id, date__range=(start_date, end_date))

            return render(request, 'hris/records.html', {'records': records, 'employee': employee})
    else:
        form = SearchForm()

    return render(request, 'hris/search.html', {'form': form})