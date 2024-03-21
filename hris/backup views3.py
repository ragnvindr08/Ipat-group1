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


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             if file.name.endswith('.csv'):
#                 data = csv.reader(file)
#             elif file.name.endswith('.xlsx'):
#                 data = xlrd.open_workbook(file_contents=file.read())
#             else:
#                 messages.error(request, 'Unsupported file format')
#                 return redirect('upload_file')

#             for row in data:
#                 employee_id, ip_address = row[0], row[1]
#                 DTR.objects.create(employee_id=employee_id, ip_address=ip_address)
            
#             messages.success(request, 'Data has been successfully uploaded.')
#             return redirect('upload_file')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})


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
            records = AttendanceRecord.objects.filter(employee_id=employee_id, date__range=(start_date, end_date))
            
            # Create a datetime object for March 1, 2024
            date_day = start_date

            # Get the day of the week (Monday is 0 and Sunday is 6)
            day_of_week = date_day.weekday()

            # Define a list of days of the week
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            
            
            convert_day = days[day_of_week]
           
            
            employee = Employee.objects.all()
            
            employee_id = None
            day = None
            official_office_in = None
            official_office_out = None
            official_honorarium_time_in = None
            official_honorarium_time_out = None
            official_servicecredit_time_in = None
            official_servicecredit_time_out = None
            official_overtime_time_in = None
            official_overtime_time_out = None
           
            official_records = OfficialTime.objects.filter(employee_id=employee_id, day=convert_day)

            if official_records.exists():
                official_record = official_records.first()  # Get the first matching record
                employee_id = official_record.employee_id
                day = convert_day
                official_office_in = official_record.official_office_in
                official_office_out = official_record.official_office_out
                official_honorarium_time_in = official_record.official_honorarium_time_in
                official_honorarium_time_out = official_record.official_honorarium_time_out
                official_servicecredit_time_in = official_record.official_servicecredit_time_in
                official_servicecredit_time_out = official_record.official_servicecredit_time_out
                official_overtime_time_in = official_record.official_overtime_time_in
                official_overtime_time_out = official_record.official_overtime_time_out
            else:
                # Handle the case where no matching record is found
                print("No OfficialTime record found for employee_id {} on {}".format(employee_id, convert_day))

                # Loop through each attendance record
            a_record = None  # Initialize with None

            time_in = None  # Initialize with None

            try:
                a_record = AttendanceRecord.objects.get(employee_id=employee_id, date=start_date)
                # Process the retrieved record
                time_in = a_record.time_in
            except AttendanceRecord.DoesNotExist:
                # Handle the case where no matching record is found
                print("No AttendanceRecord found for employee_id {} on {}".format(employee_id, start_date))

            # Now you can safely use the time_in variable
            print("Time In:", time_in)
            
            
            
            
            
            
            
            # print("Employee ID:", employee_id)
            # print("Day:", day)
            # print("Official Office In:", official_office_in)
            # print("Official Office Out:", official_office_out)
            # print("Official Honorarium Time In:", official_honorarium_time_in)
            # print("Official Honorarium Time Out:", official_honorarium_time_out)
            # print("Official Servicecredit Time In:", official_servicecredit_time_in)
            # print("Official Servicecredit Time Out:", official_servicecredit_time_out)
            # print("Official Overtime Time In:", official_overtime_time_in)
            # print("Official Overtime Time Out:", official_overtime_time_out)
            # print("Time In:", time_in)
            # print("Break In:", break_in)
            # print("Break Out:", break_out)
            # print("Time Out:", time_out)

           
            

            return render(request, 'hris/records.html', {'records': records, 'employee': employee})
    else:
        form = SearchForm()

    return render(request, 'hris/search.html', {'form': form})


from datetime import datetime, timedelta, time

# Function to compute the time difference
def compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtime_time_in,
                            official_overtime_time_out,
                            employment_status,
                            ):
    #DEFAULT TIME
    timeref = datetime.strptime("00:00", "%H:%M").time()
    # Convert strings to datetime objects if they are not empty
    if time_in:
        time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S").time()
    else:
        time_in = datetime.strptime("00:00", "%H:%M").time()

    if time_out:
        time_out_office = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S").time()
        time_out = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S").time()
    else:
        time_out_office = datetime.strptime("00:00", "%H:%M").time()   
        time_out = datetime.strptime("00:00", "%H:%M").time()
        
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in > timeref:
        time_in_hn = time_in
    else:
        time_in_hn = datetime.strptime("00:00", "%H:%M").time()
       
        
    if time_out > timeref:
        time_out_hn = time_out
    else:
        time_out_hn = datetime.strptime("00:00", "%H:%M").time()   
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in  > timeref:
        time_in_sc = time_in
    else:
        time_in_sc = datetime.strptime("00:00", "%H:%M").time()
       
        
    if time_out:
        time_out_sc = time_out
    else:
        time_out_sc = datetime.strptime("00:00", "%H:%M").time()   
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in  > timeref:
        time_in_ot = time_in
    else:
        time_in_ot = datetime.strptime("00:00", "%H:%M").time()
           
    if time_out:
        time_out_ot = time_out
    else:
        time_out_ot = datetime.strptime("00:00", "%H:%M").time()   
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------     
        
        
    if break_in:
        break_in = datetime.strptime(break_in, "%Y-%m-%d %H:%M:%S").time()
    else:
        break_in = datetime.strptime("00:00", "%H:%M").time()
        
    if break_out:
        break_out = datetime.strptime(break_out, "%Y-%m-%d %H:%M:%S").time()
    else:
        break_out = datetime.strptime("00:00", "%H:%M").time()


    # Ensure official office times are in datetime format
    official_office_in = datetime.strptime(official_office_in, "%H:%M").time()
    official_office_out = datetime.strptime(official_office_out, "%H:%M").time()
    official_honorarium_time_in = datetime.strptime(official_honorarium_time_in, "%H:%M").time()
    official_honorarium_time_out = datetime.strptime(official_honorarium_time_out, "%H:%M").time()
    official_servicecredit_time_in = datetime.strptime(official_servicecredit_time_in, "%H:%M").time()
    official_servicecredit_time_out = datetime.strptime(official_servicecredit_time_out, "%H:%M").time()
    official_overtime_time_in = datetime.strptime(official_overtime_time_in, "%H:%M").time()
    official_overtime_time_out = datetime.strptime(official_overtime_time_out, "%H:%M").time()
    timeref = datetime.strptime("00:00", "%H:%M").time()
    
    
    if employment_status == "JO":
        official_office_in_datetime = datetime.combine(datetime.today(), official_office_in)
        # Calculate the end of break time
        break_starts = official_office_in_datetime + timedelta(hours=4)
        break_end = break_starts + timedelta(hours=1)

        # Check if time_in is before official_office_in
        if time_in < official_office_in and time_in != timeref:
            time_in = official_office_in

        # Check if break_in is after break_starts
        if break_in  >= break_starts.time():
            break_in = break_starts.time()

        # Check if break_out is before break_end
        if break_out  < break_end.time():
            break_out = break_end.time()

        # Check if time_out is after official_office_out
        if time_out  > official_office_out and time_out != timeref:
            time_out_office = official_office_out
        else:
            time_out_office = time_out
       #--------HONORARIUM-------------------------------------------------------------------
       # Check if time_in is before official_office_in
        if time_in_hn != timeref:
            time_in_hn = official_honorarium_time_in

        # Check if time_out is after official_office_out
        if time_out_hn  > official_honorarium_time_out and time_out_hn != timeref:
            time_out_hn = official_honorarium_time_out          
        #------------------------------------------------------------------------------------    
        
        
        #--------SERVICE CREDIT-------------------------------------------------------------------
       # Check if time_in is before official_office_in
        if time_in != timeref:
            time_in_sc = official_servicecredit_time_in

        # Check if time_out is after official_office_out
        if time_out_sc  > official_servicecredit_time_out and time_out_sc != timeref:
            time_out_sc = official_servicecredit_time_out 
        else:
            time_out_sc = time_out               
        #------------------------------------------------------------------------------------   
        
       #--------OVER TIME-------------------------------------------------------------------
       # Check if time_in is before official_office_in
        if time_in != timeref:
            time_in_ot = official_overtime_time_in
        # Check if time_out is after official_office_out
        if time_out_ot  > official_overtime_time_out:
            time_out_ot = official_overtime_time_out    
        else:
            time_out_ot = time_out         
        #------------------------------------------------------------------------------------   

        # Calculate the difference
        if break_in and time_in != timeref:
            difference_morning = datetime.combine(datetime.today(), break_in) - datetime.combine(datetime.today(), time_in)
            # print(difference_morning)
        else:
            difference_morning = timeref
            
        if break_in and time_out_office != timeref:
            difference_afternoon = datetime.combine(datetime.today(), time_out_office) - datetime.combine(datetime.today(), break_out)
        else:
            difference_afternoon = timeref
            
        
        # Extract hours and minutes from the morning session
        if difference_morning == timeref:
            difference_hours_morning = 0
            difference_minutes_morning = 0
        else:
            difference_hours_morning = difference_morning.total_seconds() // 3600
            difference_minutes_morning = (difference_morning.total_seconds() % 3600) // 60
            
         # Extract hours and minutes from the afternoon session   
        if difference_afternoon == timeref: 
            difference_hours_afternoon = 0
            difference_minutes_afternoon = 0
        else:
            difference_hours_afternoon = difference_afternoon.total_seconds() // 3600
            difference_minutes_afternoon = (difference_afternoon.total_seconds() % 3600) // 60
            
        
        if difference_hours_morning >= 4:
            difference_minutes_morning = 0
        if difference_hours_afternoon >= 4:
            difference_minutes_afternoon = 0

        total_hours = difference_hours_morning + difference_hours_afternoon + (difference_minutes_morning + difference_minutes_afternoon) // 60
        total_minutes = (difference_minutes_morning + difference_minutes_afternoon) % 60
        
        
     

        
        #----------------------------------------COMPUTE HONORARIUM----------------------------
       
        if (time_out_hn > timeref and time_in_hn == timeref) or (time_out_hn == timeref and time_in_hn > timeref) or (time_out_hn == timeref and time_in_hn == timeref):
            
            difference_regular_hn = 0
            difference_hours_regular_hn = 0
            difference_minutes_regular_hn = 0
    
        else:
            difference_regular_hn = datetime.combine(datetime.today(), time_out_hn) - datetime.combine(datetime.today(), time_in_hn)
            difference_hours_regular_hn = difference_regular_hn.total_seconds() // 3600
            difference_minutes_regular_hn = (difference_regular_hn.total_seconds() % 3600) // 60

        #----------------------------------------COMPUTE HONORARIUM----------------------------
        
        #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
         
        if (time_out_sc > timeref and time_in_sc == timeref) or (time_out_sc== timeref and time_in_sc > timeref) or (time_out_sc == timeref and time_in_sc == timeref):

            difference_regular_sc = 0
            difference_hours_regular_sc = 0
            difference_minutes_regular_sc = 0
    
        else:

            difference_regular_sc = datetime.combine(datetime.today(), time_out_sc) - datetime.combine(datetime.today(), time_in_sc)
            difference_hours_regular_sc = difference_regular_sc.total_seconds() // 3600
            difference_minutes_regular_sc = (difference_regular_sc.total_seconds() % 3600) // 60

        #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
      

        #----------------------------------------COMPUTE OVERTIME----------------------------
         
        if (time_out_ot > official_overtime_time_in and time_in_ot != timeref):

            # Inside the COMPUTE OVERTIME block
            difference_regular_ot = datetime.combine(datetime.today(), time_out_ot) - datetime.combine(datetime.today(), time_in_ot)

            difference_hours_regular_ot = difference_regular_ot.total_seconds() // 3600
            difference_minutes_regular_ot = (difference_regular_ot.total_seconds() % 3600) // 60
            
        #----------------------------------------COMPUTE OVERTIME----------------------------
        else:

            difference_regular_ot = 0
            difference_hours_regular_ot = 0
            difference_minutes_regular_ot = 0


            



        #----------------------------------------COMPUTE OVERTIME----------------------------
        
        
        
        return difference_minutes_regular_ot,difference_hours_regular_ot, difference_minutes_regular_sc, difference_hours_regular_sc, difference_minutes_regular_hn, difference_hours_regular_hn, difference_hours_morning, difference_hours_afternoon, difference_minutes_morning, difference_minutes_afternoon, total_hours, total_minutes
        
    else:
        if (time_out_office > timeref and time_in == timeref) or (time_out_office == timeref and time_in > timeref) or (time_out_office == timeref and time_in == timeref):
            difference_regular = 0
            difference_hours_regular = 0
            difference_minutes_regular = 0
    
            return difference_minutes_regular_ot, difference_hours_regular_ot, difference_minutes_regular_sc, difference_hours_regular_sc, difference_minutes_regular_hn, difference_hours_regular_hn, difference_hours_regular, difference_minutes_regular
    
        else:


                #--------HONORARIUM-------------------------------------------------------------------
        # Check if time_in is before official_office_in
            if time_in_hn != timeref:
                time_in_hn = official_honorarium_time_in

            # Check if time_out is after official_office_out
            if time_out_hn  > official_honorarium_time_out and time_out_hn != timeref:
                time_out_hn = official_honorarium_time_out          
            #------------------------------------------------------------------------------------    
            
            
            #--------SERVICE CREDIT-------------------------------------------------------------------
        # Check if time_in is before official_office_in
            if time_in != timeref:
                time_in_sc = official_servicecredit_time_in

            # Check if time_out is after official_office_out
            if time_out_sc  > official_servicecredit_time_out and time_out_sc != timeref:
                time_out_sc = official_servicecredit_time_out 
            else:
                time_out_sc = time_out               
            #------------------------------------------------------------------------------------   
            
        #--------OVER TIME-------------------------------------------------------------------
        # Check if time_in is before official_office_in
            if time_in != timeref:
                time_in_ot = official_overtime_time_in
            # Check if time_out is after official_office_out
            if time_out_ot  > official_overtime_time_out:
                time_out_ot = official_overtime_time_out    
            else:
                time_out_ot = time_out         
            #------------------------------------------------------------------------------------   
                
             #----------------------------------------COMPUTE HONORARIUM----------------------------
       
        if (time_out_hn > timeref and time_in_hn == timeref) or (time_out_hn == timeref and time_in_hn > timeref) or (time_out_hn == timeref and time_in_hn == timeref):
            
            difference_regular_hn = 0
            difference_hours_regular_hn = 0
            difference_minutes_regular_hn = 0
    
        else:
            difference_regular_hn = datetime.combine(datetime.today(), time_out_hn) - datetime.combine(datetime.today(), time_in_hn)
            difference_hours_regular_hn = difference_regular_hn.total_seconds() // 3600
            difference_minutes_regular_hn = (difference_regular_hn.total_seconds() % 3600) // 60

        #----------------------------------------COMPUTE HONORARIUM----------------------------
        
        #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
         
        if (time_out_sc > timeref and time_in_sc == timeref) or (time_out_sc== timeref and time_in_sc > timeref) or (time_out_sc == timeref and time_in_sc == timeref):

            difference_regular_sc = 0
            difference_hours_regular_sc = 0
            difference_minutes_regular_sc = 0
    
        else:

            difference_regular_sc = datetime.combine(datetime.today(), time_out_sc) - datetime.combine(datetime.today(), time_in_sc)
            difference_hours_regular_sc = difference_regular_sc.total_seconds() // 3600
            difference_minutes_regular_sc = (difference_regular_sc.total_seconds() % 3600) // 60

            #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
        

            #----------------------------------------COMPUTE OVERTIME----------------------------
            
            if (time_out_ot > official_overtime_time_in and time_in_ot != timeref):

                # Inside the COMPUTE OVERTIME block
                difference_regular_ot = datetime.combine(datetime.today(), time_out_ot) - datetime.combine(datetime.today(), time_in_ot)

                difference_hours_regular_ot = difference_regular_ot.total_seconds() // 3600
                difference_minutes_regular_ot = (difference_regular_ot.total_seconds() % 3600) // 60
                
            #----------------------------------------COMPUTE OVERTIME----------------------------



            difference_regular = datetime.combine(datetime.today(), official_office_out) - datetime.combine(datetime.today(), time_in)
            difference_hours_regular = difference_regular.total_seconds() // 3600
            difference_minutes_regular = (difference_regular.total_seconds() % 3600) // 60

    return difference_minutes_regular_ot, difference_hours_regular_ot, difference_minutes_regular_sc, difference_hours_regular_sc, difference_minutes_regular_hn, difference_hours_regular_hn, difference_hours_regular, difference_minutes_regular,
   