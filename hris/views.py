from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .decorators import *
from .signals import *

#upload imports
import csv
import xlrd
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import datetime
from datetime import datetime, timedelta

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
    
    if official_office_in_str:
        official_office_in = official_office_in_str
        official_office_in =datetime.combine(today, official_office_in)
    else:
        official_office_in = None

    if  official_office_out_str:
        official_office_out = official_office_out_str
        official_office_out =datetime.combine(today, official_office_out)
    else:
        official_office_out = None

    if official_honorarium_time_in_str:
        official_honorarium_time_in = official_honorarium_time_in_str
        official_honorarium_time_in =datetime.combine(today, official_honorarium_time_in)
    else:
        official_honorarium_time_in = None
    
    if official_honorarium_time_out_str:
        official_honorarium_time_out = official_honorarium_time_out_str
        official_honorarium_time_out =datetime.combine(today, official_honorarium_time_out)
    else:
        official_honorarium_time_out = None
        
    if official_servicecredit_time_in_str:
        official_servicecredit_time_in = official_servicecredit_time_in_str
        official_servicecredit_time_in =datetime.combine(today, official_servicecredit_time_in)
    else:
        official_servicecredit_time_in = None

    if  official_servicecredit_time_out_str:
        official_servicecredit_time_out = official_servicecredit_time_out_str 
        official_servicecredit_time_out =datetime.combine(today, official_servicecredit_time_out)
    else:
        official_servicecredit_time_out = None
        
    if official_overtime_time_in_str:
        official_overtime_time_in = official_overtime_time_in_str   
        official_overtime_time_in =datetime.combine(today, official_overtime_time_in) 
    else:
        official_overtime_time_in = None
        
    if official_overtime_time_out_str:
        official_overtime_time_out = official_overtime_time_out_str
        official_overtime_time_out =datetime.combine(today, official_overtime_time_out) 
    else:
        official_overtime_time_out = None


        # Convert strings to datetime objects if they are not empty
    if time_in:
        office_in = time_in
        time_in = time_in
    else:
        time_in = timeref
        office_in = timeref
    if time_out:
        office_out = time_out
        time_out = time_out
    else:
        office_out = timeref
        time_out = timeref
    
    
         #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in > timeref:
        time_in_hn = time_in
    else:
        time_in_hn = timeref
       
        
    if time_out > timeref:
        time_out_hn = time_out
    else:
        time_out_hn = timeref
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in  > timeref:
        time_in_sc = time_in
    else:
        time_in_sc = timeref
       
        
    if time_out:
        time_out_sc = time_out
    else:
        time_out_sc = timeref   
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in  > timeref:
        time_in_ot = time_in
    else:
        time_in_ot = timeref
           
    if time_out:
        time_out_ot = time_out
    else:
        time_out_ot = timeref
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------     
    if employment_status == "JO":
        official_office_in_datetime = official_office_in
        official_office_out_datetime = official_office_out
                                        
        # Calculate the end of break time
        break_starts = official_office_in_datetime + timedelta(hours=4)
        break_end = break_starts + timedelta(hours=1)

        # Check if time_in is before official_office_in
        if time_in < official_office_in and time_in != timeref:
            office_in = official_office_in

        # Check if break_in is after break_starts
        if break_in  >= break_starts:
            break_in = break_starts

        # Check if break_out is before break_end
        if break_out  < break_end:
            break_out = break_end

        # Check if time_out is after official_office_out
        if time_out  > official_office_out_datetime and time_out != timeref:
            office_out = official_office_out
        else:
            office_out = time_out

        print(official_office_out,"hello")
 

        # Calculate the difference
        # Assuming break_in, office_in, break_out, and office_out are datetime objects

        # Extract time components
        break_in_time = break_in.time() if break_in else None
        time_in_time = office_in.time() if office_in else None
        break_out_time = break_out.time() if break_out else None
        time_out_time = office_out.time() if office_out else None

        # # Define current day
        # today_date = datetime.today().date()
        # break_in = break_in.strftime("%H:%M:%S") if break_in else None
        # break_out = break_out.strftime("%H:%M:%S") if break_out else None
        # office_in = office_in.strftime("%H:%M:%S") if office_in else None
        # office_out = office_out.strftime("%H:%M:%S") if office_out else None

        # # Convert to datetime objects
        # break_in = datetime.strptime(break_in, "%H:%M:%S") if break_in else None
        # break_out = datetime.strptime(break_out, "%H:%M:%S") if break_out else None
        # office_in = datetime.strptime(office_in, "%H:%M:%S") if office_in else None
        # office_out = datetime.strptime(office_out, "%H:%M:%S") if office_out else None
        # Initialize time differences as None
        difference_morning = None
        difference_afternoon = None

        # Check if break_in and time_in are not None
        if break_in and office_in is not None:
    # # Calculate difference for morning
    #         difference_morning = datetime.combine(today_date, break_in_time) - datetime.combine(today_date, time_in_time)

    #     if break_out and office_out is not None:
    #         # Calculate difference for afternoon
    #         difference_afternoon = datetime.combine(today_date, break_out_time) - datetime.combine(today_date, time_out_time)

    #     # Extract hours and minutes from the morning session
                    # Calculate the difference
            if break_in_time and time_in_time != timeref:
                difference_morning = datetime.combine(datetime.today(), break_in_time) - datetime.combine(datetime.today(), time_in_time)
                # print(difference_morning)
            else:
                difference_morning = timeref
                
            if break_out_time and time_out_time != timeref:
                difference_afternoon = datetime.combine(datetime.today(), time_out_time) - datetime.combine(datetime.today(), break_out_time)
            else:
                difference_afternoon = timeref



      # Extract hours, minutes, and seconds from the morning session
        if difference_morning == timeref:
            difference_hours_morning = 0
            difference_minutes_morning = 0
            difference_seconds_morning = 0
        else:
            difference_hours_morning = difference_morning.total_seconds() // 3600
            difference_minutes_morning = (difference_morning.total_seconds() % 3600) // 60
            difference_seconds_morning = difference_morning.total_seconds() % 60

        # Extract hours, minutes, and seconds from the afternoon session   
        if difference_afternoon == timeref: 
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

        # Calculate total hours, minutes, and seconds
        total_hours = difference_hours_morning + difference_hours_afternoon + (difference_minutes_morning + difference_minutes_afternoon) // 60
        total_minutes = (difference_minutes_morning + difference_minutes_afternoon) % 60
        total_seconds = difference_seconds_morning + difference_seconds_afternoon



        print(day)
        print(time_in_time, "time in")
        print(break_in_time, "break in")
        print(break_out_time, "break out")
        print(time_out_time, "time out")
        print(total_hours, " hours ", total_minutes, " minutes ", total_seconds," seconds")
        office_time_only_in = official_office_in.strftime("%H:%M:%S")
        # Extract time only from official_office_out
        office_time_only_out = official_office_out.strftime("%H:%M:%S")
        print(office_time_only_in)
        print(office_time_only_out)

        if official_honorarium_time_in and official_honorarium_time_out:
            official_honorarium_time_in = official_honorarium_time_in
            official_honorarium_time_out = official_honorarium_time_out
        else: 
            official_honorarium_time_in = "None"
            official_honorarium_time_out = "None"

        if official_servicecredit_time_in and official_servicecredit_time_out:
            official_servicecredit_time_in = official_servicecredit_time_in
            official_servicecredit_time_out = official_servicecredit_time_out
        else: 
            official_servicecredit_time_in = "None"
            official_servicecredit_time_out = "None"
        
        if official_overtime_time_in and official_overtime_time_out:
            official_overtime_time_in = official_overtime_time_in
            official_overtime_time_out = official_overtime_time_out
        else: 
            official_overtime_time_in = "None"
            official_overtime_time_out = "None"



    context = {
        official_office_in: official_office_in if official_office_in else "",
        official_office_out: official_office_out if official_office_out else "",

        # official_honorarium_time_in: official_honorarium_time_in if official_honorarium_time_in else "",
        # official_honorarium_time_out: official_honorarium_time_out if official_honorarium_time_out else "",

        official_servicecredit_time_in: official_servicecredit_time_in if official_servicecredit_time_in else "",
        # official_servicecredit_time_out: official_servicecredit_time_out if official_servicecredit_time_out else "",

        # official_overtime_time_in: official_overtime_time_in if official_overtime_time_in else "",
        # official_overtime_time_out: official_overtime_time_out if official_overtime_time_out else "",

        total_hours: total_hours if total_hours else "",
        total_minutes: total_minutes if total_minutes else "",
        total_seconds: total_seconds if total_seconds else "",
        day: day if day else "",
    }
    return  context

def calculate_surplus_time(surplus_time_in_str, surplus_time_out_str):
    if surplus_time_in_str and surplus_time_out_str:
        surplus_time_in = datetime.strptime(surplus_time_in_str, "%H:%M:%S")
        surplus_time_out = datetime.strptime(surplus_time_out_str, "%H:%M:%S")
        surplus_time_diff = surplus_time_out - surplus_time_in
        if surplus_time_diff > timedelta(0):
            hours = surplus_time_diff.seconds // 3600
            minutes = (surplus_time_diff.seconds % 3600) // 60
            return f"{hours} hours {minutes} minutes"
    return None


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
                    
                    if record.time_in and record.time_out:
  
                        
                                  
          
          
          

          
          

          
          
                        
                        
                        
                        
                                        
                        (record.official_office_in, 
                         record.official_office_out, 
                        #  record.official_honorarium_time_in, 
                        #  record.official_honorarium_time_out, 
                         record.official_servicecredit_time_in, 
                        #  record.official_servicecredit_time_out, 
                        #  record.official_overtime_time_in, 
                        #  record.official_overtime_time_out, 
                         record.total_hours, 
                         record.total_minutes, 
                         record.total_seconds, 
                         record.day) = calculate_time_difference(record.time_in.strftime("%H:%M:%S"),
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

                    else:
                        record.total_time = None
                
                    

                if record.surplusHour_time_in and record.surplusHour_time_out:
                    record.surplus_time = calculate_surplus_time(record.surplusHour_time_in.strftime("%H:%M:%S"), record.surplusHour_time_out.strftime("%H:%M:%S"))
                else:
                    record.surplus_time = None
      
            return render(request, 'hris/records.html', {
    'records': records, 
    'employee': employee, 
    'user_groups': user_groups, 
    'offtimes': offtimes,

})
    else:
        form = SearchForm()

    return render(request, 'hris/search.html', {'form': form})