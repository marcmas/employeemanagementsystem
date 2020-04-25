from django.db import models
from user.models import User
from django.core.exceptions import ValidationError


class Leave(models.Model):
    
    LEAVE_TYPE = (
        ('Vacation leave', 'Vacation leave'),
        ('Occasional holidays', 'Occasional holidays'),
        ('Vacation on demand', 'Vacation on demand'),
        ('Vacation childcare', 'Vacation childcare'),
        ('Unpaid leave', 'Unpaid leave'),
    )

    STATUS = (
        ('Accept', 'Accepted'),
        ('Pending', 'Pending'),
        ('Reject', 'Rejected')
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    leave_type = models.CharField(max_length=100, null=True, choices=LEAVE_TYPE)
    leave_date = models.DateField(auto_now=False)
    return_date = models.DateField(auto_now=False)
    days = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=100, default='Pending', null=True, blank=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.leave_type + "-" + self.employee.first_name + "-" + self.employee.last_name + "-" + str(self.days)

    def get_accept_url(self):
        return "/{}/accept_leave".format(self.id)

    def get_detail_url(self):
        return "/{}/detail_leave".format(self.id)

    def get_reject_url(self):
        return "/{}/reject_leave".format(self.id)


class AcceptLeave(models.Model):
    leave = models.OneToOneField(Leave, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.status


class RejectLeave(models.Model):
    leave = models.OneToOneField(Leave, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.status


class VacationLimit(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    normal_days_constant = models.IntegerField(null=True, blank=True)
    normal_days = models.IntegerField(null=True, blank=True)
    children_days_constant = models.IntegerField(null=True, blank=True)
    children_days = models.IntegerField(null=True, blank=True)
    request_days_constant = models.IntegerField(null=True, blank=True)
    request_days = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.employee)


class LeaveNotificationEmployee(models.Model):

    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    notification = models.TextField(null=True)
    read = models.BooleanField(default=False)
    date_read = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.leave.employee.first_name + " " + self.notification