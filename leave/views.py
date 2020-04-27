from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Leave, VacationLimit, AcceptLeave, RejectLeave, LeaveNotificationEmployee
from user.decorators import unauthenticated_user, allowed_users, admin_only, check_regulation
from .forms import CreateLeaveForm, CreateAcceptLeaveForm, CreateRejectLeaveForm, UpdateVacationLimitForm, ExportLeaveForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from user.models import SalaryInfo
from documents.models import RegulationsStatus

# Paginations
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# For xls export
import xlwt
# Messages
from django.contrib import messages
# For count days
import numpy as np
# Change date 
import datetime

@allowed_users(allowed_roles=['employee', 'supervisor'])
def export_leave_xls(request):
    form = ExportLeaveForm()
    if request.method == 'POST':

        user = request.user

        leave_date = request.POST.get('leave_date')
        return_date = request.POST.get('return_date')
   

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Leaves-{}-{}.xls"'.format(user.first_name, user.last_name)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Leaves')

        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Type leave', 'Leave date', 'Return date', 'Count days', 'Comment', 'Status']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = Leave.objects.filter(Q(employee=user) & Q(leave_date__range=(leave_date, return_date)) & Q(return_date__range=(leave_date, return_date))).values_list('leave_type', 'leave_date', 'return_date', 'days', 'comment', 'status')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                # Change date format in excel
                if col_num == 1 or col_num == 2:
                    font_style.num_format_str = 'D-MM-YYYY'
                else:
                    font_style.num_format_str = '0'
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        if not rows:
            messages.warning(request, "In this range you doesn't have a holidays")
            return redirect('/export_leave_xls')
        else:
            return response

    context = {
        'form': form
    }
    template_name = "leave/export_leave_xls.html"
    return render(request, template_name, context)

@allowed_users(allowed_roles=['supervisor', 'admin'])
def export_employyes_leaves_xls(request):
   
    file_name = datetime.datetime.today().strftime("%Y-%m-%d")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Leaves-{}.xls"'.format(file_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Leaves')

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['First name', 'Last name', 'Type leave', 'Leave date', 'Return date', 'Count days', 'Comment', 'Status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Leave.objects.filter(employee__userprofile__boss=request.user.boss).values_list('employee__first_name', 'employee__last_name', 'leave_type', 'leave_date', 'return_date', 'days', 'comment', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            # Change date format in excel
            if col_num == 3 or col_num == 4:
                font_style.num_format_str = 'D-MM-YYYY'
            else:
                font_style.num_format_str = '0'
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    if not rows:
        messages.warning(request, "Employees dosn't have a holidays")
        return redirect('/export_leave_xls')
    else:
        return response


@allowed_users(allowed_roles=['supervisor', 'admin'])
def export_employyes_limits_xls(request):
   
    file_name = datetime.datetime.today().strftime("%Y-%m-%d")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="VacationLimits-{}.xls"'.format(file_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Limits')

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['First name', 'Last name', 'Normal days costant', 'Normal days', 'Children days costant', 'Children days', 'Request days costant', 'Request days']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = VacationLimit.objects.filter(employee__userprofile__boss=request.user.boss).values_list('employee__first_name', 'employee__last_name', 'normal_days_constant', 'normal_days', 'children_days_constant', 'children_days', 'request_days_constant', 'request_days')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    if not rows:
        messages.warning(request, "You doesn't have any employees")
        return redirect('/export_leave_xls')
    else:
        return response


@allowed_users(allowed_roles=['employee', 'supervisor'])
def addLeave(request, *args):
    user = request.user
    vacation_limits = VacationLimit.objects.get(employee=user)
    user_leaves = Leave.objects.filter(employee=user)
    form = CreateLeaveForm()

    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        return_date = request.POST.get('return_date')
        leave_type = request.POST.get('leave_type')

        leave_date = datetime.datetime.strptime(leave_date, '%Y-%m-%d').date()
        return_date = datetime.datetime.strptime(return_date, '%Y-%m-%d').date()
        check = True

        # Check if user has a leaves in given dates
        if user_leaves:
            for leave in user_leaves:
                if leave_date <= leave.leave_date <= return_date:
                    check = False
            # If user hasn't a leaves in given dates
            if check:
                holiday_days = np.busday_count(leave_date, return_date) + 1
                # Check all types of leaves
                if leave_type == 'Vacation leave':
                    if vacation_limits.normal_days >= holiday_days:
                        form = CreateLeaveForm(request.POST or None)
                        if form.is_valid():
                            form.instance.employee = user
                            form.instance.days = holiday_days
                            form.save()
                            messages.success(request, "You request has been send")
                            return redirect('/list_leaves')
                    else:
                        messages.warning(request, "You don't have enough days")
                elif leave_type == 'Vacation childcare':
                    if vacation_limits.children_days >= holiday_days:
                        form = CreateLeaveForm(request.POST or None)
                        if form.is_valid():
                            form.instance.employee = user
                            form.instance.days = holiday_days
                            form.save()
                            messages.success(request, "You request has been send")
                            return redirect('/list_leaves')
                    else:
                        messages.warning(request, "You don't have enough days")
                elif leave_type == 'Vacation on demand':
                    if vacation_limits.request_days >= holiday_days:
                        form = CreateLeaveForm(request.POST or None)
                        if form.is_valid():
                            form.instance.employee = user
                            form.instance.days = holiday_days
                            form.save()
                            messages.success(request, "You request has been send")
                            return redirect('/list_leaves')
                    else:
                        messages.warning(request, "You don't have enough days")
                else:
                    form = CreateLeaveForm(request.POST or None)
                    if form.is_valid():
                        form.instance.employee = user
                        form.instance.days = holiday_days
                        form.save()
                        messages.success(request, "You request has been send")
                        return redirect('/list_leaves')
            else:
                messages.warning(request, "You have leave in these days")
        else:
            holiday_days = np.busday_count(leave_date, return_date) + 1
            if vacation_limits.normal_days > holiday_days:
                form = CreateLeaveForm(request.POST or None)
                if form.is_valid():
                    form.instance.employee = user
                    form.instance.days = holiday_days
                    form.save()
                    messages.success(request, "You request has been send")
                    return redirect('/list_leaves')

    context = {
        'form': form,
        'user_leaves': user_leaves,
    }

    return render(request, 'leave/add_leave.html', context)


def calendar(request):
    context = {}
    template_name = 'leave/calendar.html'
    return render(request, template_name, context)


@allowed_users(allowed_roles=['employee', 'supervisor'])
def listLeaves(request, *args):
    user = request.user
    emplooyee_leaves = Leave.objects.filter(employee=user)

    context = {
        'emplooyee_leaves': emplooyee_leaves
    }

    return render(request, 'leave/list_leave.html', context)


@allowed_users(allowed_roles=['employee', 'supervisor'])
def detailVacationLimits(request):
    user = request.user
    vacation_limits = VacationLimit.objects.get(employee=user.id)
    hour_normal_days = vacation_limits.normal_days_constant * 8
    template_name = 'leave/detail_vacation_limits.html'

    context = {
        'vacation_limits': vacation_limits,
        'hour_normal_days': hour_normal_days,
    }

    return render(request, template_name, context)


@allowed_users(allowed_roles=['hr', 'admin'])
def updateVacationLimitPage(request, user_id):
    user = User.objects.get(id=user_id)
    form = UpdateVacationLimitForm(request.POST or None, instance=user.vacationlimit)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated')
            return redirect('/{}/view_user_info/'.format(user.id))

    context = {
        'form': form,
    }
    return render(request, 'leave/update/update_vacation_limit.html', context)


@allowed_users(allowed_roles=['supervisor', 'admin'])
def detailLeave(request, leave_id):

    unique_leave = get_object_or_404(Leave, id=leave_id)

    template_name = 'leave/detail_leave.html'

    context = {
        'unique_leave': unique_leave
    }

    return render(request, template_name, context)


@allowed_users(allowed_roles=['supervisor', 'admin'])
def acceptLeave(request, leave_id):
    unique_leave = get_object_or_404(Leave, id=leave_id, employee__userprofile__boss=request.user.boss)
    vacation_limit = VacationLimit.objects.get(employee=unique_leave.employee)
    check_leave = AcceptLeave.objects.filter(leave=unique_leave).exists()
    form = CreateAcceptLeaveForm()
    if not check_leave:
        if request.method == "POST":
            if vacation_limit.normal_days >= unique_leave.days:
                form = CreateAcceptLeaveForm(request.POST or None)
                form.instance.status = "Accept"
                form.instance.leave = unique_leave
                if form.is_valid():
                    form.save()
                    messages.success(request, "Leave has been accepted successfully")
                    return redirect('/{}/detail_leave'.format(leave_id))
            else:
                messages.warning(request, "Employee doesn't has enought days")
                return redirect('/{}/detail_leave'.format(leave_id))
    context = {
        'form': form,
    }
    return render(request, 'leave/accept_leave.html', context)


@allowed_users(allowed_roles=['supervisor', 'admin'])
def rejectLeave(request, leave_id):
    unique_leave = get_object_or_404(Leave, id=leave_id, employee__userprofile__boss=request.user.boss)
    check_leave = RejectLeave.objects.filter(leave=unique_leave).exists()
    form = CreateRejectLeaveForm()
    if not check_leave:
        if request.method == "POST":
            form = CreateRejectLeaveForm(request.POST or None)
            form.instance.status = "Reject"
            form.instance.leave = unique_leave
            if form.is_valid():
                form.save()
                messages.success(request, "Leave has been rejected successfully")
                return redirect('/{}/detail_leave'.format(leave_id))

    context = {
        'form': form,
    }
    
    return render(request, 'leave/reject_leave.html', context)


@allowed_users(allowed_roles=['admin', 'supervisor'])
def viewPendingLeaves(request, *args):
    emplooyee_leaves = Leave.objects.filter(employee__userprofile__boss=request.user.boss).filter(status='Pending')

    context = {
        'emplooyee_leaves': emplooyee_leaves
    }

    return render(request, 'leave/view_pending_leave.html', context)


@allowed_users(allowed_roles=['admin', 'supervisor'])
def viewAcceptedLeaves(request, *args):
    emplooyee_leaves = Leave.objects.filter(employee__userprofile__boss=request.user.boss).filter(status='Accept')

    context = {
        'emplooyee_leaves': emplooyee_leaves
    }

    return render(request, 'leave/view_accepted_leave.html', context)


@allowed_users(allowed_roles=['admin', 'supervisor'])
def viewRejectedLeaves(request, *args):
    emplooyee_leaves = Leave.objects.filter(employee__userprofile__boss=request.user.boss).filter(status='Reject')

    context = {
        'emplooyee_leaves': emplooyee_leaves
    }

    return render(request, 'leave/view_rejected_leave.html', context)


@allowed_users(allowed_roles=['supervisor', 'admin'])
def viewListEmployeesLimits(request, *args):
    employees = User.objects.filter(userprofile__boss=request.user.boss).exclude(id=request.user.id)
    context = {
        'employees': employees
    }

    return render(request, 'leave/view_list_employees_limits.html', context)


@allowed_users(allowed_roles=['supervisor', 'admin'])
def viewEmployeesLimits(request, employee_id):
    vacation_limits = VacationLimit.objects.get(employee=employee_id)
    leaves = Leave.objects.filter(employee=employee_id).order_by('-date_created')

    context = {
        'vacation_limits': vacation_limits,
        'leaves': leaves
    }

    return render(request, 'leave/view_employees_limits.html', context)


@allowed_users(allowed_roles=['supervisor', 'admin', 'employee', 'hr'])
def acceptNotification(request, notification_id):
    user = request.user
    now= datetime.datetime.now()
    unique_notification = get_object_or_404(LeaveNotificationEmployee, id=notification_id)
    if unique_notification.read == True:
        return redirect("/notifications")
    if unique_notification.read == False:
        if unique_notification.user == user:
            unique_notification.read = True
            unique_notification.date_read = now
            unique_notification.save()
            return redirect("/notifications")
        else:
            return HttpResponse("This page isn't for you")


@allowed_users(allowed_roles=['supervisor', 'admin', 'employee', 'hr'])
def viewNotifications(request):
    user = request.user
    
    notificat = LeaveNotificationEmployee.objects.filter(user=user).order_by('-date_created')
    paginator = Paginator(notificat, 20)

    page = request.GET.get('page')
    try:
        notificat = paginator.page(page)
    except PageNotAnInteger:
        notificat = paginator.page(1)
    except EmptyPage:
        notificat = paginator.page(paginator.num_pages)

    context = {
        'notificat': notificat,
    }

    return render(request, 'leave/view_notifications.html', context)


# Dashobords
@allowed_users(allowed_roles=['admin', 'employee', 'hr', 'supervisor'])
@check_regulation
def dashboard(request, **kwargs):
    user = request.user

    # Notifications
    notificat = LeaveNotificationEmployee.objects.filter(user=user).order_by('-date_created')[:15]
    paginator = Paginator(notificat, 4)

    page = request.GET.get('page')
    try:
        notificat = paginator.page(page)
    except PageNotAnInteger:
        notificat = paginator.page(1)
    except EmptyPage:
        notificat = paginator.page(paginator.num_pages)

    # Documents
    documents = RegulationsStatus.objects.filter(employee=user)
    pagin = Paginator(documents, 2)

    page = request.GET.get('page_documents')
    try:
        documents = pagin.page(page)
    except PageNotAnInteger:
        documents = pagin.page(1)
    except EmptyPage:
        documents = pagin.page(pagin.num_pages)  

    context = {
        'notificat': notificat,
        'documents': documents,
        'user': user
    }
    
    return render(request, 'ems/dashboard.html', context)


# Leave Json File
def jsonPendingLeave(request):
    user = request.user
    user_leaves = Leave.objects.filter(employee=user).filter(status='Pending')

    if user_leaves:
        data = []
        for l in user_leaves:
            data.append({'title': l.leave_type, 'start': l.leave_date, 'end': l.return_date + datetime.timedelta(days=1)})
    else:
        data = [{}]

    return JsonResponse(data, safe=False)
    

def jsonAcceptedLeave(request):
    user = request.user
    user_leaves = Leave.objects.filter(employee=user).filter(status='Accept')


    if user_leaves:
        leave = []
        for l in user_leaves:
            leave.append({'title': l.leave_type, 'start': l.leave_date, 'end': l.return_date + datetime.timedelta(days=1) })
    else:
        leave = [{}]
    
    print(leave)

    return JsonResponse(leave, safe=False)


def jsonRejectedLeave(request):
    user = request.user
    user_leaves = Leave.objects.filter(employee=user).filter(status='Reject')


    if user_leaves:
        leave = []
        for l in user_leaves:
            leave.append({'title': l.leave_type, 'start': l.leave_date, 'end': l.return_date + datetime.timedelta(days=1)})
    else:
        leave = [{}]

    return JsonResponse(leave, safe=False)