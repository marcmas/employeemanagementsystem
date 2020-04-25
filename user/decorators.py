from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from documents.models import RegulationsStatus
from django.db.models import Q


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = Group.objects.get(user=request.user).name
            return redirect('/dashboard')
            # if group == 'admin':
            #     return redirect('/admin/dashboard')
            # elif group == 'hr':
            #     return redirect('/hr/dashboard')
            # elif group == 'employee':
            #     return redirect('/employee/dashboard')
            # elif group == 'supervisor':
            #     return redirect('/supervisor/dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

                
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                response = render(request, 'ems/404.html')
                response.status_code = 404
                return response
        return wrapper_func
    return decorator


def check_regulation(view_func):
    def wrapper_func(request, *args, **kwargs):
        if RegulationsStatus.has_noaccept_necessary_regulation.filter(employee=request.user).exists():
            regulation = RegulationsStatus.has_noaccept_necessary_regulation.filter(employee=request.user).first()
            return redirect('/{}/detail_regulation_user'.format(regulation.regulation.id))
        else:
            return view_func(request, *args, **kwargs)            
    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group != 'admin':
            response = render(request, 'ems/404.html')
            response.status_code = 404
            return response
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func
