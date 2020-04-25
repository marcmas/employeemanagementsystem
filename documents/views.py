from django.shortcuts import render, redirect
# Models
from .models import Regulations, RegulationsStatus
# Forms
from .forms import CreateRegulationForm
# Allowed users
from user.decorators import allowed_users
# Messages
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Datetime 
import datetime


@allowed_users(allowed_roles=['hr'])
def addRegulation(request):
    form = CreateRegulationForm()

    if request.method == 'POST':
        form = CreateRegulationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Regulations has been added successfully')
            return redirect('/view_list_regulations')

    context = {
        'form': form
    }

    template_name = 'documents/add_regulation.html'
    return render(request, template_name, context)


@allowed_users(allowed_roles=['hr','admin'])
def viewListRegulations(request):
    regulations = Regulations.objects.all()

    context = {
        'regulations': regulations
    }
    template_name = 'documents/view_list_regulations.html'
    return render(request, template_name, context)


@allowed_users(allowed_roles=['hr', 'admin'])
def viewDetailRegulation(request, regulation_id):
    regulation = Regulations.objects.get(id=regulation_id)

    context = {
        'regulation': regulation
    }
    template_name = 'documents/view_detial_regulation.html'
    return render(request, template_name, context)


@allowed_users(allowed_roles=['employee', 'supervisor'])
def viewListRegulationsForUser(request):

    regulations = RegulationsStatus.objects.filter(employee=request.user)

    context = {
        'regulations': regulations
    }
    
    template_name = 'documents/view_list_regulations_user.html'
    return render(request, template_name, context)


@allowed_users(allowed_roles=['employee', 'supervisor'])
def viewDetailRegulationForUsers(request, regulation_id):

    regulation = {}

    try:
        regulation = RegulationsStatus.objects.get(Q(regulation__id=regulation_id) & Q(employee=request.user))
    except ObjectDoesNotExist:
        response = render(request, 'ems/404.html')
        response.status_code = 404
        return response

    context = {
        'regulation': regulation
    }
    template_name = 'documents/view_detial_regulation_for_users.html'
    return render(request, template_name, context)


@allowed_users(allowed_roles=['employee', 'supervisor'])
def acceptRegulation(request, regulation_id):
    regulation = RegulationsStatus.objects.get(Q(regulation__id=regulation_id) & Q(employee=request.user))


    if regulation:  
        regulation.accept = True
        regulation.accept_date = datetime.datetime.today()
        regulation.save()
        messages.success(request, 'Regulations has been aceepted successfully')
        return redirect('/{}/detail_regulation_user/'.format(regulation.regulation.id))
    else:
        response = render(request, 'ems/404.html')
        response.status_code = 404
        return response
