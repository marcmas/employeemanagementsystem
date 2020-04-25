from django.shortcuts import render, redirect, HttpResponse
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm, UpdateUserProfileForm, LoginForm, UpdateUserForm, UpdateUsernameForm, UpdateSalaryInfoForm, UpdateUserProfileEmployeeForm, UpdateBankInfoForm, updateProfilePictureForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import User, Group

from .models import UserProfile, Boss
from django.db.models import Q
from django.urls import reverse

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.contrib.auth.decorators import login_required
import random

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@allowed_users(allowed_roles=['hr'])
def addEmployeePage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)

            # Set a new password
            password = User.objects.make_random_password(length=9, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
            user.set_password(password)
            user.save()

            # Add user to group
            group_name = request.POST.get('group_name')
            g = Group.objects.get(name=group_name)
            g.user_set.add(user)

            # Add model Boss if role supervisor
            group_name = Group.objects.get(user=user).name
            if group_name == 'supervisor':
                Boss.objects.create(
                    user=user,
                )

            # redirect to update user page with message
            username = form.cleaned_data.get('username')
            messages.success(request,  'Account was created for ' + username + '. New password for ' + username + ' it ' + password)
            return redirect('/{}/update_userprofile_info/'.format(user.id))


    groups = Group.objects.all().exclude(Q(name='admin'))
    context = {
        'form': form,
        'groups': groups
    }
    return render(request, 'user/add_user.html', context)


@allowed_users(allowed_roles=['hr', 'admin', 'supervisor'])
def downloadUserPassword(request, user_id):
    user = User.objects.get(id=user_id)
    # Set a new password
    password = User.objects.make_random_password(length=9, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
    user.set_password(password)
    user.save()

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(20, 800, "Password: {}  Username: {} ".format(password, user.username))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='{}{}.pdf'.format(user.first_name, user.last_name))


@allowed_users(allowed_roles=['hr', 'admin', 'supervisor'])
def viewUser(request, user_id):
    user = User.objects.get(id=user_id)

    context = {
        'user': user,
    }

    return render(request, 'user/detail_change_user.html', context)


@allowed_users(allowed_roles=['hr', 'admin'])
def updateBaseInfoPage(request, user_id):
    user = User.objects.get(id=user_id)

    form = UpdateUserForm(request.POST or None, instance=user)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated')
            return redirect('/{}/view_user_info/'.format(user.id))

    context = {
        'form': form,
    }
    return render(request, 'user/update/update_base_info.html', context)


@allowed_users(allowed_roles=['hr', 'admin'])
def updateProfilePicturePage(request, user_id):
    user = User.objects.get(id=user_id)

    form = updateProfilePictureForm(request.POST or None, request.FILES or None, instance=user.userprofile)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated')
            return redirect('/{}/view_user_info/'.format(user.id))

    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'user/update/update_profile_picture.html', context)


@allowed_users(allowed_roles=['hr', 'admin'])
def deleteUserPage(request, user_id):
    user = User.objects.get(id=user_id)
    
    messages.success(request, 'User {} {} has been deleted'.format(user.first_name, user.last_name))
    user.delete()
    return redirect('/users/')


@allowed_users(allowed_roles=['hr', 'admin', 'employee', 'supervisor'])
def activityPage(request):
    user = request.user
    
    context = {
        'user': user
    }

    return render(request, 'user/activity_log.html', context)


@allowed_users(allowed_roles=['hr', 'admin'])
def updateUserprofileInfoPage(request, user_id):
    user = User.objects.get(id=user_id)
    group = user.groups.all()[0]

    if 'employee' == str(group):
        form = UpdateUserProfileEmployeeForm(request.POST or None, instance=user.userprofile)
    else:
        form = UpdateUserProfileForm(request.POST or None, instance=user.userprofile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated')
            return redirect('/{}/view_user_info/'.format(user.id))

    context = {
        'form': form,
    }
    return render(request, 'user/update/update_userprofile_info.html', context)


@allowed_users(allowed_roles=['hr', 'admin'])
def updateSalaryInfoPage(request, user_id):
    user = User.objects.get(id=user_id)

    form = UpdateSalaryInfoForm(request.POST or None, instance=user.salaryinfo)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated')
            return redirect('/{}/view_user_info/'.format(user.id))

    context = {
        'form': form,
    }
    return render(request, 'user/update/update_salaryinfo_info.html', context)


@allowed_users(allowed_roles=['hr', 'admin'])
def updateBankInfoPage(request, user_id):
    user = User.objects.get(id=user_id)
    form = UpdateBankInfoForm(request.POST or None, instance=user.bankinfo)



    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated')
            return redirect('/{}/view_user_info/'.format(user.id))

    context = {
        'form': form,
    }
    return render(request, 'user/update/update_bankinfo_info.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user:
                login(request, user)
                return redirect('/dashboard/')
            else:
                messages.info(request, 'Username or password is incorrect')
        
    context = {
        'form': LoginForm()
    }
    return render(request, 'user/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')


@allowed_users(allowed_roles=['admin', 'supervisor', 'hr'])
def users(request):
    userGroup = Group.objects.get(user=request.user).name

    # Filter only users who are related with supervisor by the SECTION 
    if userGroup == 'supervisor':
        users_all = User.objects.filter(groups__name='employee').filter(userprofile__boss=request.user.boss)
    # Admin can view all users in the database
    elif userGroup == 'admin':
        users_all = User.objects.exclude(id=request.user.id).all()
    # Admin can view all users in the database
    elif userGroup == 'hr':
        users_all = User.objects.exclude(id=request.user.id).all()
    # If users isn't a admin, hr or supervisor then redirect to dashbaord page
    else:
        return redirect('/dashboard')

    paginator = Paginator(users_all, 12)

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'users': users,
    }

    return render(request, 'user/users.html', context)


@login_required
def infoUser(request):
    user = request.user.id
    user = User.objects.get(id=user)

    context = {
        'user': user,
    }

    return render(request, 'user/info_about_you.html', context)


@login_required
def settingsPage(request):
    context = {}

    template = 'user/settings_page.html'

    return render(request, template, context)


@login_required
def changeUsername(request):
    template = 'user/change_username.html'
    form = UpdateUsernameForm(request.POST)
    if request.method == "POST":
        form = UpdateUsernameForm(request.POST or None)
        if form.is_valid():
            user = request.user
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if user.check_password(password1) and user.check_password(password2):
                user.username = username
                user.save()
                messages.success(request, "Your username has been changed successfully")
                return redirect('/settings_page')


    context = {
        'form': form,
    }


    return render(request, template, context)