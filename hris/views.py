from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only
from .signals import *

from django.conf import settings
import os
# Create your views here.


# def registerPage(request):
#     if request.user.is_authenticated:
#         form = CreateUserForm()
#         groups = Group.objects.all()
#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 username = form.cleaned_data.get('username')
              
            
#                 messages.success(request,'Account was created for ' + username)

#                 return redirect('register')

#         context = {'form':form}
#         return render(request, 'hris/register.html', context)

# def registerPage(request):
#     if request.user.is_authenticated:
#         form = CreateUserForm()
#         groups = Group.objects.all()  # Retrieve all groups from the database

#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 username = form.cleaned_data.get('username')
#                 selected_group_name = request.POST.get('group')  # Get the selected group name from the form data
#                 group = Group.objects.get(name=selected_group_name)  # Get the group object based on the selected group name
#                 user.groups.add(group)  # Add the user to the selected group
#                 messages.success(request, 'Account was created for ' + username)
#                 return redirect('register')

#         context = {'form': form, 'groups': groups}  # Pass the groups to the template context
#         return render(request, 'hris/register.html', context)
#     else:
#         return redirect('login')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .forms import CreateUserForm

# def registerPage(request):
#     if request.user.is_authenticated:
#         form = CreateUserForm()
#         groups = Group.objects.all()

#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 username = form.cleaned_data.get('username')
#                 group_name = request.POST.get('group')  # Retrieve the selected group name from the form
#                 if group_name:
#                     group = Group.objects.get(name=group_name)  # Retrieve the group object
#                     user.groups.add(group)  # Add the user to the group
#                 messages.success(request, 'Account was created for ' + username)
#                 return redirect('register')

#         context = {'form': form, 'groups': groups}
#         return render(request, 'hris/register.html', context)
#     else:
#         return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        form = CreateUserForm()
        groups = Group.objects.all()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group_name = request.POST.get('group')  # Retrieve the selected group name from the form
                if group_name:
                    group = Group.objects.get(name=group_name)  # Retrieve the group object
                    user.groups.add(group)  # Add the user to the group
                
                # Check if an Employee profile already exists for the user
                employee_profile, created = Employee.objects.get_or_create(user=user)

                # If an Employee profile is created, fill in additional fields if needed
                if created:
                    # Fill in additional fields if needed
                    pass
                
                messages.success(request, 'Account was created for ' + username)
                return redirect('register')

        context = {'form': form, 'groups': groups}
        return render(request, 'hris/register.html', context)
    else:
        return redirect('login')



    
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
# @admin_only
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