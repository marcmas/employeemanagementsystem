from django import template
from django.contrib.auth.models import User
from user.models import SalaryInfo
from leave.models import Leave

register = template.Library() 

@register.simple_tag
def employee_count(request):
    user = request.user
    return User.objects.filter(userprofile__boss__user=user).count()

@register.simple_tag
def salary_info(request):
    user = request.user
    return SalaryInfo.objects.get(employee=user).salary

@register.simple_tag
def accepted_leave_info(request):
    user = request.user
    return Leave.objects.filter(employee=user).filter(status='Accept').count()

@register.simple_tag
def pending_leave_info(request):
    user = request.user
    return Leave.objects.filter(employee=user).filter(status='Pending').count()

@register.simple_tag
def rejected_leave_info(request):
    user = request.user
    return Leave.objects.filter(employee=user).filter(status='Rejected').count()

# @register.simple_tag
# def show_results(value):
#     user = request.user
#     return LeaveNotification.objects.filter(leave_employee=value)

