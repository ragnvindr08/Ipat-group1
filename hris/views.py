from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .decorators import *
from .signals import *
from django.db.models import Q
#upload imports
import csv
import xlrd
import datetime
from datetime import datetime, timedelta
from django.urls import reverse  # Import reverse here
from django.conf import settings
import os
from django.forms import modelformset_factory
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.http import HttpResponse
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
                            time_only = date_time_parts[1]
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
                        default_time = time(hour=0, minute=0, second=0)
                        # Assigning time components to the appropriate fields based on column values
                        # Note: I assume you want to save the full date_time string for time-related fields
                        if time_only:  # Check if date_time is not empty
                            if column1 == 1 and column2 == 0 and column3 == 1 and column4 == 0:      
                                    record.time_in = time_only
                            elif column1 == 1 and column2 == 1 and column3 == 1 and column4 == 0:
                                record.break_in = time_only
                            elif column1 == 1 and column2 == 4 and column3 == 1 and column4 == 0:
                                record.break_out = time_only
                            elif column1 == 1 and column2 == 5 and column3 == 1 and column4 == 0:
                                record.time_out = time_only
                            elif column1 == 1 and column2 == 4 and column3 == 0 and column4 == 0:
                                if  record.time_in != default_time:
                                    record.time_in = time_only
                                else:
                                    record.surplusHour_time_in = time_only    
                            elif column1 == 1 and column2 == 5 and column3 == 0 and column4 == 0:
                                if record.time_out != default_time:
                                    record.time_out = time_only
                                else:
                                    record.surplusHour_time_out = time_only

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
                    # Update existing employee profile with new employee number and employment_status
                    employee_profile.employee_id = employee_number
                    employee_profile.employment_status = group_name
                    employee_profile.save()
                except Employee.DoesNotExist:
                        # Create new employee profile if it doesn't exist
                    employee_profile = Employee.objects.create(
                    user=user,
                    employee_id=employee_number,
                    first_name=user.first_name,
                    surname=user.last_name,
                    employment_status=group_name
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



def calculate_time_difference(time_in_str, time_out_str, break_in_str, break_out_str, 
                              day_str,
                              employent_status_str,
                              official_office_in_str,
                              official_office_out_str,
                              official_honorarium_time_in_str,
                              official_honorarium_time_out_str,
                              official_servicecredit_time_in_str,
                              official_servicecredit_time_out_str,
                              official_overtime_time_in_str,
                              official_overtime_time_out_str
                              ):
    
    today = datetime.now().date()

    # Convert time strings to datetime objects
    timeref = datetime.strptime("00:00:00", "%H:%M:%S")
    time_in = datetime.strptime(time_in_str, "%H:%M:%S")
    break_in = datetime.strptime(break_in_str, "%H:%M:%S")
    break_out = datetime.strptime(break_out_str, "%H:%M:%S")
    time_out = datetime.strptime(time_out_str, "%H:%M:%S")

    # Convert time objects to datetime objects with today's date
    time_in = datetime.combine(today, time_in.time())
    break_in = datetime.combine(today, break_in.time())
    break_out = datetime.combine(today, break_out.time())
    time_out = datetime.combine(today, time_out.time())
    day = day_str
    employment_status = employent_status_str
    midnight = time(0, 0)  # Represents 00:00:00
    datetime_with_midnight = datetime.combine(today, midnight) 

    if official_office_in_str:
        official_office_in = official_office_in_str
        official_office_in =datetime.combine(today, official_office_in)
    else:
        official_office_in = datetime_with_midnight

    if  official_office_out_str:
        official_office_out = official_office_out_str
        official_office_out =datetime.combine(today, official_office_out)
    else:
        official_office_out = datetime_with_midnight

    if official_honorarium_time_in_str:
        official_honorarium_time_in = official_honorarium_time_in_str
        official_honorarium_time_in =datetime.combine(today, official_honorarium_time_in)
    else:
        official_honorarium_time_in = datetime_with_midnight
    
    if official_honorarium_time_out_str:
        official_honorarium_time_out = official_honorarium_time_out_str
        official_honorarium_time_out =datetime.combine(today, official_honorarium_time_out)
    else:
        official_honorarium_time_out = datetime_with_midnight
        
    if official_servicecredit_time_in_str:
        official_servicecredit_time_in = official_servicecredit_time_in_str
        official_servicecredit_time_in =datetime.combine(today, official_servicecredit_time_in)
    else:
        official_servicecredit_time_in = datetime_with_midnight

    if  official_servicecredit_time_out_str:
        official_servicecredit_time_out = official_servicecredit_time_out_str 
        official_servicecredit_time_out =datetime.combine(today, official_servicecredit_time_out)
    else:
        official_servicecredit_time_out = datetime_with_midnight
        
    if official_overtime_time_in_str:
        official_overtime_time_in = official_overtime_time_in_str   
        official_overtime_time_in =datetime.combine(today, official_overtime_time_in) 
    else:
        official_overtime_time_in = datetime_with_midnight
        
    if official_overtime_time_out_str:
        official_overtime_time_out = official_overtime_time_out_str
        official_overtime_time_out =datetime.combine(today, official_overtime_time_out) 
    else:
        official_overtime_time_out = datetime_with_midnight


        # Convert strings to datetime objects if they are not empty
    if time_in:
        office_in = time_in
        time_in = time_in
    else:
        time_in = datetime_with_midnight
        office_in = datetime_with_midnight
    if time_out:
        office_out = time_out
        time_out = time_out
    else:
        office_out = datetime_with_midnight
        time_out = datetime_with_midnight
    

         #----------------HONO-----------------------------------------------------------------
   
    if time_in > datetime_with_midnight and time_in <= official_honorarium_time_in:
        time_in_hn = official_honorarium_time_in
    else:
        time_in_hn = time_in
       
        
    if time_out > official_honorarium_time_out:
        time_out_hn = official_honorarium_time_out
    else:
        if time_out < official_servicecredit_time_in:
            time_in_hn = datetime_with_midnight
            time_out_hn = datetime_with_midnight
        else:
            time_out_hn = time_out   
        
        
        #----------------HONO-------------------END--------------------------------------------
        #-----------------SC---------------------------------------------------------------------
   
    if time_in  > datetime_with_midnight and time_in <= official_servicecredit_time_in  and time_out > official_servicecredit_time_in:
        time_in_sc = official_servicecredit_time_in
    else:
        time_in_sc = time_in
       
        
    if time_out > official_servicecredit_time_out:
        time_out_sc = official_servicecredit_time_out
    else:
        
        if time_out < official_servicecredit_time_in:
            time_in_sc = datetime_with_midnight
            time_out_sc = datetime_with_midnight
        else:
            time_out_sc = time_out   
        
        
        
        #-----------------SC-------------------END--------------------------------------------
        #-------------------OT----------------------------------------------------------------
   
    if time_in  > datetime_with_midnight and time_in <= official_overtime_time_in:
        time_in_ot = official_overtime_time_in
    else:
        time_in_ot = time_in
           
    if time_out > official_overtime_time_out:
        time_out_ot = official_overtime_time_out
    else:
        if time_out < official_servicecredit_time_in:
            time_in_ot = datetime_with_midnight
            time_out_ot = datetime_with_midnight
        else:
            time_out_ot = time_out  
    
        #--------------------OT-----------------END--------------------------------------------     
    if employment_status == "FACULTY":
        midnight = time(0, 0)  # Represents 00:00:00
        datetime_with_midnight = datetime.combine(today, midnight)   
        official_office_in_datetime = official_office_in

        official_office_out_datetime = official_office_out
        time_object = time(0, 0, 0)
        time_object2 = datetime.combine(datetime.today(), time_object)
        time_object_replace = time(12, 0, 0)
        time_object_replace2 = datetime.combine(datetime.today(), time_object_replace)
        if official_office_in_datetime > time_object2:             
        # Calculate the end of break time
            break_starts = official_office_in_datetime + timedelta(hours=4)
            break_end = break_starts + timedelta(hours=1)
        else:
            break_starts =time_object2
            break_end = time_object2

        faculty_official_office_in = official_office_in_datetime.time() if official_office_in_datetime else None
        office_in = time_in.time() if time_in else None
        office_out = time_out.time() if time_out else None
        faculty_official_office_out = official_office_out_datetime.time() if official_office_out_datetime else None
        
        if time_in < official_office_in and time_in != timeref:
            office_in = official_office_in_datetime

        # Check if time_out is after official_office_out
        if time_out  > official_office_out_datetime and time_out != time_object2:
            office_out = official_office_out_datetime
        else:
            office_out = time_out




        difference_faculty = office_out - datetime.combine(datetime.today(), office_in)
        difference_hours_faculty = difference_faculty.total_seconds() // 3600
        difference_minutes_faculty = (difference_faculty.total_seconds() % 3600) // 60
        difference_seconds_faculty = difference_faculty.total_seconds() % 60

        total_hours = difference_hours_faculty
        total_minutes = difference_minutes_faculty % 60
        total_seconds = difference_seconds_faculty


        tardiness_difference_faculty = (datetime.combine(datetime.today(), office_in) - datetime.combine(datetime.today(), faculty_official_office_in)) + (datetime.combine(datetime.today(), faculty_official_office_out) - office_out)
        tardiness_difference_hours_faculty = tardiness_difference_faculty.total_seconds() // 3600
        tardiness_difference_minutes_faculty = (tardiness_difference_faculty.total_seconds() % 3600) // 60
        tardiness_difference_seconds_faculty = tardiness_difference_faculty.total_seconds() % 60

        tardiness_total_hours = tardiness_difference_hours_faculty
        tardiness_total_minutes = tardiness_difference_minutes_faculty % 60
        tardiness_total_seconds = tardiness_difference_seconds_faculty
        print( tardiness_total_hours," tardiness_total_hours")

        if official_office_in_datetime == datetime_with_midnight:
            official_office_in = "N/A"
            total_hours = 0
            total_minutes = 0
            total_seconds = 0
            tardiness_total_hours = 0
        else:
            official_office_in = official_office_in_datetime.time()


        if official_office_out_datetime == datetime_with_midnight:
            official_office_out = "N/A"
            total_hours = 0
            total_minutes = 0
            total_seconds = 0
            tardiness_total_hours = 0
            
        else:
            official_office_out = official_office_out_datetime.time()
        



              
   
        if official_honorarium_time_in > time_object2 and official_honorarium_time_out > time_object2:
            official_honorarium_time_in = official_honorarium_time_in
            official_honorarium_time_out = official_honorarium_time_out
        else: 
            official_honorarium_time_in = time_object2
            official_honorarium_time_out = time_object2

        if official_servicecredit_time_in> time_object2 and official_servicecredit_time_out > time_object2:
            official_servicecredit_time_in = official_servicecredit_time_in
            official_servicecredit_time_out = official_servicecredit_time_out
        else: 
            official_servicecredit_time_in = time_object2
            official_servicecredit_time_out = time_object2
        
        if official_overtime_time_in > time_object2 and official_overtime_time_out > time_object2:
            official_overtime_time_in = official_overtime_time_in
            official_overtime_time_out = official_overtime_time_out
        else: 
            official_overtime_time_in = time_object2
            official_overtime_time_out = time_object2


#----------------------------------------COMPUTE HONORARIUM----------------------------
       
        if (time_out_hn > datetime_with_midnight and time_in_hn == datetime_with_midnight) or (time_out_hn == datetime_with_midnight and time_in_hn > datetime_with_midnight) or (time_out_hn == datetime_with_midnight and time_in_hn == datetime_with_midnight):
            
            difference_hn = 0
            difference_hours_hn = 0
            difference_minutes_hn = 0
            difference_seconds_hn = 0
    
        else:
            difference_hn = time_out_hn - time_in_hn
            difference_hours_hn = difference_hn.total_seconds() // 3600
            difference_minutes_hn = (difference_hn.total_seconds() % 3600) // 60
            difference_seconds_hn = difference_hn.total_seconds() % 60


        tardiness_difference_hn =  0
        tardiness_difference_hours_hn = 0
        tardiness_difference_minutes_hn = 0
        tardiness_difference_seconds_hn = 0

        if (official_honorarium_time_in and official_honorarium_time_out) and (official_honorarium_time_in !=datetime_with_midnight and official_honorarium_time_out != datetime_with_midnight ):

            tardiness_difference_hn =  (  time_in_hn - official_honorarium_time_in) + (  official_honorarium_time_out - time_out_hn)
            tardiness_difference_hours_hn = tardiness_difference_hn.total_seconds() // 3600
            tardiness_difference_minutes_hn = (tardiness_difference_hn.total_seconds() % 3600) // 60
            tardiness_difference_seconds_hn = tardiness_difference_hn.total_seconds() % 60
            print(tardiness_difference_hn,"tardiness_difference_hn")

        if difference_hours_hn < 0:
            tardiness_difference_hours_hn =  official_honorarium_time_out - official_honorarium_time_in
            tardiness_difference_minutes_hn = 0
            tardiness_difference_seconds_hn = 0
            difference_hn = 0
            difference_hours_hn = 0
            difference_minutes_hn = 0
            difference_seconds_hn = 0
            tardiness_difference_hours_hn  = int(tardiness_difference_hours_hn.total_seconds() // 3600)
  
            

        # + (  official_honorarium_time_out - time_out_hn)

        #----------------------------------------COMPUTE HONORARIUM----------------------------
        
        #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
         
        if (time_out_sc > timeref and time_in_sc == datetime_with_midnight) or (time_out_sc== datetime_with_midnight and time_in_sc > datetime_with_midnight) or (time_out_sc == datetime_with_midnight and time_in_sc == datetime_with_midnight):

            difference_sc = 0
            difference_hours_sc = 0
            difference_minutes_sc = 0
            difference_seconds_sc = 0
    
        else:

            difference_sc = time_out_sc - time_in_sc
            difference_hours_sc = difference_sc.total_seconds() // 3600
            difference_minutes_sc = (difference_sc.total_seconds() % 3600) // 60
            difference_seconds_sc = difference_sc.total_seconds() % 60


        tardiness_difference_sc =  0
        tardiness_difference_hours_sc = 0
        tardiness_difference_minutes_sc = 0
        tardiness_difference_seconds_sc = 0

        if (official_servicecredit_time_in and official_servicecredit_time_out) and (official_servicecredit_time_in !=datetime_with_midnight and official_servicecredit_time_out != datetime_with_midnight ):

            tardiness_difference_sc =  (  time_in_sc - official_servicecredit_time_in) + (  official_servicecredit_time_out - time_out_sc)
            tardiness_difference_hours_sc = tardiness_difference_sc.total_seconds() // 3600
            tardiness_difference_minutes_sc = (tardiness_difference_sc.total_seconds() % 3600) // 60
            tardiness_difference_seconds_sc = tardiness_difference_sc.total_seconds() % 60
            #print(tardiness_difference_seconds_sc,"tardiness_difference_hn")

        if tardiness_difference_hours_sc < 0:
            tardiness_difference_hours_sc =  official_servicecredit_time_out - official_servicecredit_time_in
            tardiness_difference_minutes_sc = 0
            tardiness_difference_seconds_sc = 0
           # print(tardiness_difference_hours_hn,"tardiness_difference_hours_hn")
            #tardiness_difference_hours_hn = datetime.strptime('2024-04-04 03:00:00', '%Y-%m-%d %H:%M:%S')

            # Extracting hours from the given datetime
            tardiness_difference_hours_sc = tardiness_difference_hours_sc.hour
        # + (  official_honorarium_time_out - time_out_hn)


            #----------------------------------------COMPUTE SERVICE CREDIT----------------------------    

            #----------------------------------------COMPUTE OVERTIME----------------------------
            
     
        if (time_out_ot > datetime_with_midnight and time_in_ot == datetime_with_midnight) or (time_out_ot == datetime_with_midnight and time_in_ot > datetime_with_midnight) or (time_out_ot == datetime_with_midnight and time_in_ot == datetime_with_midnight):
            
            difference_ot = 0
            difference_hours_ot = 0
            difference_minutes_ot = 0
            difference_seconds_ot = 0
    
        else:
            difference_ot = time_out_ot - time_in_ot
            difference_hours_ot = difference_ot.total_seconds() // 3600
            difference_minutes_ot = (difference_ot.total_seconds() % 3600) // 60
            difference_seconds_ot = difference_ot.total_seconds() % 60


        tardiness_difference_ot =  0
        tardiness_difference_hours_ot = 0
        tardiness_difference_minutes_ot = 0
        tardiness_difference_seconds_ot = 0

        if (official_overtime_time_in and official_overtime_time_out) and (official_overtime_time_in !=datetime_with_midnight and official_overtime_time_out != datetime_with_midnight ):

            tardiness_difference_ot =  (  time_in_ot - official_overtime_time_in) + (  official_overtime_time_out - time_out_ot)
            tardiness_difference_hours_ot = tardiness_difference_ot.total_seconds() // 3600
            tardiness_difference_minutes_ot = (tardiness_difference_ot.total_seconds() % 3600) // 60
            tardiness_difference_seconds_ot = tardiness_difference_ot.total_seconds() % 60
            print(tardiness_difference_ot,"tardiness_difference_ot")

        if difference_hours_ot < 0:
            tardiness_difference_hours_ot =  official_overtime_time_out - official_overtime_time_in
            tardiness_difference_minutes_ot = 0
            tardiness_difference_seconds_ot = 0
            difference_ot = 0
            difference_hours_ot = 0
            difference_minutes_ot = 0
            difference_seconds_ot = 0
            tardiness_difference_hours_ot  = int(tardiness_difference_hours_ot.total_seconds() // 3600)
            
        #----------------------------------------COMPUTE OVERTIME----------------------------

        break_in1 = datetime_with_midnight
        break_out1 = datetime_with_midnight


        if break_out == time_object2:
            break_out = break_end
            break_out1 = time_object2
        else:
            break_out = break_out
            break_out1 = break_out

        if break_in == time_object2:
            break_in = break_starts
            break_in1 = time_object2
        else:
            break_in = break_in
            break_in1 = break_in
        

        if break_in1 == datetime_with_midnight:
            break_in1 = "N/A"
        else:
            break_in1 = break_in.time()


        if break_out1 == datetime_with_midnight:
            break_out1 = "N/A"
        else:
            break_out1 = break_out.time()
            #NA IF HONORARIUM IS EMPTY
        if official_honorarium_time_in == datetime_with_midnight:
            official_honorarium_time_in = "N/A"
        else:
            official_honorarium_time_in = official_honorarium_time_in.time()

        if official_honorarium_time_out == datetime_with_midnight:
            official_honorarium_time_out = "N/A"
        else:
            official_honorarium_time_out = official_honorarium_time_out.time()

            #NA IF SC IS EMPTY
        if official_servicecredit_time_in == datetime_with_midnight:
            official_servicecredit_time_in = "N/A"
        else:
            official_servicecredit_time_in = official_servicecredit_time_in.time()

        if official_servicecredit_time_out == datetime_with_midnight:
            official_servicecredit_time_out = "N/A"
        else:
            official_servicecredit_time_out = official_servicecredit_time_out.time()      

                    #NA IF OT IS EMPTY
        if official_overtime_time_in == datetime_with_midnight:
            official_overtime_time_in = "N/A"
        else:
            official_overtime_time_in = official_overtime_time_in.time()

        if official_overtime_time_out == datetime_with_midnight:
            official_overtime_time_out = "N/A"
        else:
            official_overtime_time_out = official_overtime_time_out.time()
        
       



        return tardiness_difference_hours_ot, tardiness_difference_minutes_ot, tardiness_difference_seconds_ot, tardiness_difference_hours_sc, tardiness_difference_minutes_sc, tardiness_difference_seconds_sc, tardiness_difference_hours_hn, tardiness_difference_minutes_hn, tardiness_difference_seconds_hn, tardiness_total_seconds, tardiness_total_minutes, tardiness_total_hours, difference_hours_hn, difference_minutes_hn, difference_seconds_hn, difference_hours_sc, difference_minutes_sc, difference_seconds_sc,difference_hours_ot, difference_minutes_ot, difference_seconds_ot,official_honorarium_time_in, official_honorarium_time_out, official_servicecredit_time_in, official_servicecredit_time_out, official_overtime_time_in, official_overtime_time_out, break_in1, break_out1,official_office_in_datetime, official_office_out_datetime, official_office_in ,official_office_out, total_hours, total_minutes, total_seconds, day
        
    else:
        official_office_in_datetime = official_office_in
        official_office_out_datetime = official_office_out
        deduction_time = 0
        time_object = time(0, 0, 0)
        time_object2 = datetime.combine(datetime.today(), time_object)

        time_object_replace = time(12, 0, 0)
        time_object_replace2 = datetime.combine(datetime.today(), time_object_replace)


        if official_office_in_datetime > time_object2:             
        # Calculate the end of break time
            break_starts = official_office_in_datetime + timedelta(hours=4)
            break_end = break_starts + timedelta(hours=1)
        else:
            break_starts =time_object2
            break_end = time_object2   

        # Check if time_in is before official_office_in
        if time_in < official_office_in and time_in > time_object2:
            office_in = official_office_in

        # Check if break_in is after break_starts
        if break_in  < break_starts and break_in != time_object2:
            break_in_time = break_in
        else:
            break_in_time = break_starts

        # Check if break_out is before break_end
        if break_out  > break_end:
            break_out_time = break_out
        else:
            break_out_time = break_end

        # Check if time_out is after official_office_out
        if time_out  > official_office_out_datetime :
            office_out = official_office_out
        else:
            office_out = time_out


        if break_in == time_object2 or break_out == time_object2:
            deduction_time = 1
        
        break_in1 = None
        break_out1 = None
        

        if break_out == time_object:
            break_out_time = break_end
            break_out1 = time_object
        else:
            break_out = break_out
            break_out1 = break_out

        if break_in == time_object:
            break_in_time = break_starts
            break_in1 = time_object
        else:
            break_in = break_in
            break_in1 = break_in




        # Initialize time differences as None
        difference_morning = None
        difference_afternoon = None
        
        # Check if break_in and time_in are not None
        # if break_in and office_in is not None:
        
        break_in_time = break_in_time.time() if break_in_time else break_starts
        time_in_time = office_in.time() if office_in else time_object2
        break_out_time = break_out_time.time() if break_out_time else break_end
        time_out_time = office_out.time() if office_out else time_object2  







        if break_in_time and time_in_time != time_object:
            difference_morning = datetime.combine(datetime.today(), break_in_time) - datetime.combine(datetime.today(), time_in_time)


        else:
            difference_morning = time_object
            
        if break_out_time and time_out_time != time_object:
            difference_afternoon = datetime.combine(datetime.today(), time_out_time) - datetime.combine(datetime.today(), break_out_time)
        else:
            difference_afternoon = time_object


      # Extract hours, minutes, and seconds from the morning session
        if difference_morning == time_object:
            difference_hours_morning = 0
            difference_minutes_morning = 0
            difference_seconds_morning = 0
        else:
            difference_hours_morning = difference_morning.total_seconds() // 3600
            difference_minutes_morning = (difference_morning.total_seconds() % 3600) // 60
            difference_seconds_morning = difference_morning.total_seconds() % 60

        # Extract hours, minutes, and seconds from the afternoon session   
        if difference_afternoon == time_object: 
            difference_hours_afternoon = 0
            difference_minutes_afternoon = 0
            difference_seconds_afternoon = 0
        else:
            difference_hours_afternoon = difference_afternoon.total_seconds() // 3600
            difference_minutes_afternoon = (difference_afternoon.total_seconds() % 3600) // 60
            difference_seconds_afternoon = difference_afternoon.total_seconds() % 60

        # Reset minutes if hours are greater than or equal to 4
        if difference_hours_morning >= 4:
            difference_minutes_morning = 0
        if difference_hours_afternoon >= 4:
            difference_minutes_afternoon = 0


        midnight = time(0, 0)  # Represents 00:00:00
# Combine the current date with the midnight time
        datetime_with_midnight = datetime.combine(today, midnight)
        if official_office_in_datetime == datetime_with_midnight or official_office_out_datetime == datetime_with_midnight:
            difference_hours_afternoon = 0
            difference_minutes_afternoon = 0
            difference_seconds_afternoon = 0
            difference_hours_morning = 0
            difference_minutes_morning = 0
            difference_seconds_morning = 0

        # Calculate total hours, minutes, and seconds
        total_hours = (difference_hours_morning + difference_hours_afternoon + (difference_minutes_morning + difference_minutes_afternoon) // 60) - deduction_time
        total_minutes = (difference_minutes_morning + difference_minutes_afternoon) % 60
        total_seconds = difference_seconds_morning + difference_seconds_afternoon
        
   
        if official_honorarium_time_in > time_object2 and official_honorarium_time_out > time_object2:
            official_honorarium_time_in = official_honorarium_time_in
            official_honorarium_time_out = official_honorarium_time_out
        else: 
            official_honorarium_time_in = time_object2
            official_honorarium_time_out = time_object2

        if official_servicecredit_time_in> time_object2 and official_servicecredit_time_out > time_object2:
            official_servicecredit_time_in = official_servicecredit_time_in
            official_servicecredit_time_out = official_servicecredit_time_out
        else: 
            official_servicecredit_time_in = time_object2
            official_servicecredit_time_out = time_object2
        
        if official_overtime_time_in > time_object2 and official_overtime_time_out > time_object2:
            official_overtime_time_in = official_overtime_time_in
            official_overtime_time_out = official_overtime_time_out
        else: 
            official_overtime_time_in = time_object2
            official_overtime_time_out = time_object2

        print("---------------------------------------------------------------------")

        
   #----------------------------------------COMPUTE HONORARIUM----------------------------
       
        if (time_out_hn > datetime_with_midnight and time_in_hn == datetime_with_midnight) or (time_out_hn == datetime_with_midnight and time_in_hn > datetime_with_midnight) or (time_out_hn == datetime_with_midnight and time_in_hn == datetime_with_midnight):
            
            difference_hn = 0
            difference_hours_hn = 0
            difference_minutes_hn = 0
            difference_seconds_hn = 0
    
        else:
            difference_hn = time_out_hn - time_in_hn
            difference_hours_hn = difference_hn.total_seconds() // 3600
            difference_minutes_hn = (difference_hn.total_seconds() % 3600) // 60
            difference_seconds_hn = difference_hn.total_seconds() % 60

        #----------------------------------------COMPUTE HONORARIUM----------------------------
        
        #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
         
        if (time_out_sc > timeref and time_in_sc == datetime_with_midnight) or (time_out_sc== datetime_with_midnight and time_in_sc > datetime_with_midnight) or (time_out_sc == datetime_with_midnight and time_in_sc == datetime_with_midnight):

            difference_sc = 0
            difference_hours_sc = 0
            difference_minutes_sc = 0
            difference_seconds_sc = 0
    
        else:

            difference_sc = time_out_sc - time_in_sc
            difference_hours_sc = difference_sc.total_seconds() // 3600
            difference_minutes_sc = (difference_sc.total_seconds() % 3600) // 60
            difference_seconds_sc = difference_sc.total_seconds() % 60

            #----------------------------------------COMPUTE SERVICE CREDIT----------------------------    

            #----------------------------------------COMPUTE OVERTIME----------------------------
            
        if (time_out_ot > timeref and time_in_ot == datetime_with_midnight) or (time_out_ot== datetime_with_midnight and time_in_ot > datetime_with_midnight) or (time_out_ot == datetime_with_midnight and time_in_ot == datetime_with_midnight):
            difference_ot = 0
            difference_hours_ot = 0
            difference_minutes_ot = 0
            difference_seconds_ot = 0
        else:
            # Inside the COMPUTE OVERTIME block
            difference_ot = time_out_ot - time_in_ot
            difference_hours_ot = difference_ot.total_seconds() // 3600
            difference_minutes_ot = (difference_ot.total_seconds() % 3600) // 60
            difference_seconds_ot = difference_ot.total_seconds() % 60
            
        #----------------------------------------COMPUTE OVERTIME----------------------------
        if official_office_in_datetime == datetime_with_midnight:
            official_office_in_datetime = "N/A"
            total_hours = 0
            total_minutes = 0
            total_seconds = 0
        else:
            official_office_in_datetime = official_office_in_datetime.time()


        if official_office_out_datetime == datetime_with_midnight:
            official_office_out_datetime = "N/A"
            total_hours = 0
            total_minutes = 0
            total_seconds = 0
        else:
            official_office_out_datetime = official_office_out_datetime.time()

        if break_in1 == datetime_with_midnight:
            break_in1 = "N/A"
        else:
            break_in1 = break_in.time()


        if break_out1 == datetime_with_midnight:
            break_out1 = "N/A"
        else:
            break_out1 = break_out.time()
            
            #NA IF HONORARIUM IS EMPTY
        if official_honorarium_time_in == datetime_with_midnight:
            official_honorarium_time_in = "N/A"
        else:
            official_honorarium_time_in = official_honorarium_time_in.time()

        if official_honorarium_time_out == datetime_with_midnight:
            official_honorarium_time_out = "N/A"
        else:
            official_honorarium_time_out = official_honorarium_time_out.time()

            #NA IF SC IS EMPTY
        if official_servicecredit_time_in == datetime_with_midnight:
            official_servicecredit_time_in = "N/A"
        else:
            official_servicecredit_time_in = official_servicecredit_time_in.time()

        if official_servicecredit_time_out == datetime_with_midnight:
            official_servicecredit_time_out = "N/A"
        else:
            official_servicecredit_time_out = official_servicecredit_time_out.time()      

                    #NA IF OT IS EMPTY
        if official_overtime_time_in == datetime_with_midnight:
            official_overtime_time_in = "N/A"
        else:
            official_overtime_time_in = official_overtime_time_in.time()

        if official_overtime_time_out == datetime_with_midnight:
            official_overtime_time_out = "N/A"
        else:
            official_overtime_time_out = official_overtime_time_out.time()   

            
            
            
        return  difference_hours_hn, difference_minutes_hn, difference_seconds_hn, difference_hours_sc, difference_minutes_sc, difference_seconds_sc,difference_hours_ot, difference_minutes_ot, difference_seconds_ot,official_honorarium_time_in, official_honorarium_time_out, official_servicecredit_time_in, official_servicecredit_time_out, official_overtime_time_in, official_overtime_time_out, break_in1, break_out1, official_office_in_datetime,official_office_out_datetime, total_hours,total_minutes,total_seconds, day
    
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
            
            # Fetch the groups the current user belongs to
            user_groups = request.user.groups.all()
            
            

            for record in records:
                # Convert start_date to string and then to datetime object
                start_date_tostr = str(start_date)
                date_convert = datetime.strptime(start_date_tostr, "%Y-%m-%d")
                
                # Get the day of the week
                day_of_week = date_convert.strftime("%A")
                
                # Fetch official times based on employee ID and day of the week
                all_offtimes = OfficialTime.objects.filter(employee_id=employee_id)
               
                # Now you can iterate over fetched official times and perform operations
                day_of_week = record.date.strftime("%A")

                # Filter OfficialTime objects for the specific day
                offtimes = all_offtimes.filter(day=day_of_week)

                if offtimes.exists():
                    offtime = offtimes.first()  # Assuming there's only one OfficialTime object for each day
                    # Access attributes of the OfficialTime object
                    officialday = offtime.day
                    emptstats = employee.employment_status
                    officialTimeIn = offtime.official_office_in
                    offtimeout = offtime.official_office_out
                    offhnin = offtime.official_honorarium_time_in
                    offhnout = offtime.official_honorarium_time_out
                    offscin = offtime.official_servicecredit_time_in
                    offscout = offtime.official_servicecredit_time_out
                    offotin = offtime.official_overtime_time_in
                    offotout = offtime.official_overtime_time_out
                    
                    if emptstats != "FACULTY":

                        record.difference_hours_hn, record.difference_minutes_hn, record.difference_seconds_hn, record.difference_hours_sc, record.difference_minutes_sc, record.difference_seconds_sc, record.difference_hours_ot, record.difference_minutes_ot, record.difference_seconds_ot, record.official_honorarium_time_in, record.official_honorarium_time_out, record.official_servicecredit_time_in, record.official_servicecredit_time_out, record.official_overtime_time_in, record.official_overtime_time_out, record.break_in1, record.break_out1, record.official_office_in_datetime,  record.official_office_out_datetime, record.total_hours, record.total_minutes, record.total_seconds, record.day = calculate_time_difference(record.time_in.strftime("%H:%M:%S"),
                                                                    record.time_out.strftime("%H:%M:%S"),
                                                                    record.break_in.strftime("%H:%M:%S"),
                                                                    record.break_out.strftime("%H:%M:%S"),
                                                                    officialday,
                                                                    emptstats,
                                                                    officialTimeIn,
                                                                    offtimeout,
                                                                    offhnin,
                                                                    offhnout,
                                                                    offscin,
                                                                    offscout,
                                                                    offotin,
                                                                    offotout                                                                    
                                                                    )



                    else:
                        
                         record.tardiness_difference_hours_ot, record.tardiness_difference_minutes_ot, record.tardiness_difference_seconds_ot, record.tardiness_difference_hours_sc, record.tardiness_difference_minutes_sc, record.tardiness_difference_seconds_sc, record.tardiness_difference_hours_hn, record.tardiness_difference_minutes_hn, record.tardiness_difference_seconds_hn, record.tardiness_total_seconds, record.tardiness_total_minutes, record.tardiness_total_hours,record.difference_hours_hn, record.difference_minutes_hn, record.difference_seconds_hn, record.difference_hours_sc, record.difference_minutes_sc, record.difference_seconds_sc, record.difference_hours_ot, record.difference_minutes_ot, record.difference_seconds_ot, record.official_honorarium_time_in, record.official_honorarium_time_out, record.official_servicecredit_time_in, record.official_servicecredit_time_out, record.official_overtime_time_in, record.official_overtime_time_out, record.break_in1, record.break_out1,record.official_office_in_datetime,record.official_office_out_datetime, record.official_office_in_datetime, record.official_office_out_datetime, record.total_hours, record.total_minutes, record.total_seconds, record.day = calculate_time_difference(record.time_in.strftime("%H:%M:%S"),
                                                                    record.time_out.strftime("%H:%M:%S"),
                                                                    record.break_in.strftime("%H:%M:%S"),
                                                                    record.break_out.strftime("%H:%M:%S"),
                                                                    officialday,
                                                                    emptstats,
                                                                    officialTimeIn,
                                                                    offtimeout,
                                                                    offhnin,
                                                                    offhnout,
                                                                    offscin,
                                                                    offscout,
                                                                    offotin,
                                                                    offotout                                                                    
                                                                    )
                        
                        

                                    # Update record's total time components


            return render(request, 'hris/records.html', {
            'records': records, 
            'employee': employee, 
            'user_groups': user_groups, 
            'offtimes': offtimes,

                                })
    else:
        form = SearchForm()

    return render(request, 'hris/search.html', {'form': form})



def search_attendance(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        employee = get_object_or_404(Employee, employee_id=employee_id)
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Generate date range
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        # Query the database for attendance records within the date range and employee ID
        attendance_records = {}
        for day in date_range:
            records = AttendanceRecord.objects.filter(
                employee_id=employee_id,
                date=day
            )
            attendance_records[day] = records

        return render(request, 'hris/search_results.html', {'attendance_records': attendance_records, 'date_range': date_range, 'start_date': start_date, 'end_date': end_date, 'employee':employee})
    

    return render(request, 'hris/search_attendance.html')



def search_attendance_record(request):
    if request.method == 'POST':
        form = AttendanceSearchForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            # Convert datetime.date objects to strings
            start_date_str = start_date.strftime('%B %d, %Y')
            end_date_str = end_date.strftime('%B %d, %Y')

            # Convert start_date and end_date to the desired format (YYYY-MM-DD)
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')

            records = AttendanceRecord.objects.filter(
                employee_id=employee_id,
                date__range=[start_date, end_date]
            )
            if records.exists():  # Check if there are any matching records
                first_record = records.first()  # Retrieve the first record from the queryset
                old_time_in = first_record.time_in
                print(old_time_in)
            else:
                print("No attendance record found for the specified criteria")

            # Pass start_date and end_date to the template
            return render(request, 'hris/attendance_records.html', {'records': records, 'start_date': start_date_str, 'end_date': end_date_str})
    else:
        # Check if there is stored form data in session
        stored_form_data = request.session.pop('search_form_data', None)
        if stored_form_data:
            # Use stored form data to pre-populate the form
            form = AttendanceSearchForm(stored_form_data)
        else:
            form = AttendanceSearchForm()

    return render(request, 'hris/search_attendance_record.html', {'form': form})


@login_required
def edit_attendance_record(request, record_id, start_date=None, end_date=None):
    record = get_object_or_404(AttendanceRecord, id=record_id)
    initial_record = {
        'employee_id': record.employee_id,
        'date': record.date,
        'time_in': record.time_in,
        'break_in': record.break_in,
        'break_out': record.break_out,
        'time_out': record.time_out,
        'surplusHour_time_in': record.surplusHour_time_in,
        'surplusHour_time_out': record.surplusHour_time_out,
    }
    start_date = start_date if start_date else request.GET.get('start_date')
    end_date = end_date if end_date else request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%B %d, %Y')

    # Format the datetime object to 'YYYY-MM-DD' format
    start_date = start_date.strftime('%Y-%m-%d')
    
    end_date = datetime.strptime(end_date, '%B %d, %Y')

    # Format the datetime object to 'YYYY-MM-DD' format
    end_date = end_date.strftime('%Y-%m-%d')

    old_time_in = initial_record['time_in']
    old_break_in = initial_record['break_in']
    old_break_out = initial_record['break_out']
    old_time_out = initial_record['time_out']
    old_surplusHour_time_in = initial_record['surplusHour_time_in']
    old_surplusHour_time_out = initial_record['surplusHour_time_out']

    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            edited_record = form.save()
            # Save log entry
            log_data = f"Employee ID: {edited_record.employee_id}\n"
            log_data += f"Date: {edited_record.date}\n"
            log_data += f"Time In: {old_time_in} -> {edited_record.time_in}\n"
            log_data += f"Break In: {old_break_in} -> {edited_record.break_in}\n"
            log_data += f"Break Out: {old_break_out} -> {edited_record.break_out}\n"
            log_data += f"Time Out: {old_time_out} -> {edited_record.time_out}\n"
            log_data += f"Surplus Hour Time In: {old_surplusHour_time_in} -> {edited_record.surplusHour_time_in}\n"
            log_data += f"Surplus Hour Time Out: {old_surplusHour_time_out} -> {edited_record.surplusHour_time_out}\n"
            log_data += f"Edited By: {request.user.username}\n"

            EditLogs.objects.create(
                attendance_record=edited_record,
                edited_by=request.user,
                logged_data=log_data
            )

            # Redirect to the attendance_records view with search parameters
            return HttpResponseRedirect(reverse('attendance_records') + f'?employee_id={edited_record.employee_id}&start_date={start_date}&end_date={end_date}')
    else:
        form = AttendanceRecordForm(instance=record, initial=initial_record)
    
    # Pass start_date and end_date to the template context


    return render(request, 'hris/edit_record.html', {'form': form, 'record': record, 'start_date': start_date, 'end_date': end_date})




def view_attendance_records(request):
    # Retrieve search parameters from the request
    employee_id = request.GET.get('employee_id')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Parse the dates in the format '%Y-%m-%d'
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        # Handle invalid date format, for example, redirect to a page with an error message
        return HttpResponse("Invalid date format")

    # Query the database to retrieve attendance records based on the search parameters
    records = AttendanceRecord.objects.filter(
        employee_id=employee_id,
        date__range=[start_date, end_date]
    )

    # Render the attendance_records.html template with the retrieved records
    return render(request, 'hris/attendance_records.html', {'records': records, 'start_date': start_date, 'end_date': end_date})
