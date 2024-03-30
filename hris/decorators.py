from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


# def admin_only(view_func):
#     def wrapper_func(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name

#             if group == 'customer':
#                 return redirect('user-page')
#             if group == 'admin':
#                 return view_func(request, *args, **kwargs)
#     return wrapper_func



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.is_authenticated:
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in ['JO','EMPLOYEE','FACULTY']:
                return redirect('user-page')
            elif  group in ['ADMIN','HR','ACCOUNTING']:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        else:
            return redirect('login')
    return wrapper_func