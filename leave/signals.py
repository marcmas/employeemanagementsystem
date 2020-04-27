from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import VacationLimit, Leave, AcceptLeave, RejectLeave, LeaveNotificationEmployee


def employee_vacation_limit(sender, instance, created, **kwargs):
    if created:
        VacationLimit.objects.create(
            employee = instance,
            normal_days = 26,
            children_days = 0, 
            request_days = 4,
            normal_days_constant = 26,
            children_days_constant = 0, 
            request_days_constant = 4,
            )

post_save.connect(employee_vacation_limit, sender=User)


def substract_vacation_limits(sender, instance, created, **kwargs):
    if created:
        limits = VacationLimit.objects.get(employee=instance.leave.employee.id)
        if instance.leave.leave_type == 'Vacation leave':
            limits.normal_days -= instance.leave.days
            limits.save()
            if limits.normal_days < 4:
                limits.request_days = limits.normal_days
                limits.save()
        elif instance.leave.leave_type == 'Vacation childcare':
            limits.children_days -= instance.leave.days
            limits.save()
        elif instance.leave.leave_type == 'Vacation on demand':
            limits.request_days -=  instance.leave.days
            limits.normal_days -= instance.leave.days
            limits.save()
        else:
            pass


post_save.connect(substract_vacation_limits, sender=AcceptLeave)


def accept_leave_status(sender, instance, created, **kwargs):
    if created:
        if not instance.leave.status == 'Accept' or not instance.leave.status == 'Reject':
            if instance.leave.status == 'Pending':
                instance.leave.status = 'Accept'
                instance.leave.save()

post_save.connect(accept_leave_status, sender=AcceptLeave)


def reject_leave_status(sender, instance, created, **kwargs):
    if created:
        if not instance.leave.status == 'Accept' or not instance.leave.status == 'Reject':
            if instance.leave.status == 'Pending':
                instance.leave.status = 'Reject'
                instance.leave.save()

post_save.connect(reject_leave_status, sender=RejectLeave)

# signals notifications
def notification_accept_leave(sender, instance, created, **kwargs):
    if created:
        LeaveNotificationEmployee.objects.create(
            leave=instance.leave,
            user=instance.leave.employee,
            notification = "Your request for absence {} from {} to {} has been approved by your supervisor / coordinator".format(instance.leave.leave_type, instance.leave.leave_date, instance.leave.return_date),
        )
        LeaveNotificationEmployee.objects.create(
            leave=instance.leave,
            user=instance.leave.employee.userprofile.boss.user,
            notification = "You accepted the request for absence {} from {} to {}.".format(instance.leave.leave_type, instance.leave.leave_date, instance.leave.return_date),
        )

post_save.connect(notification_accept_leave, sender=AcceptLeave)


def notification_reject_leave(sender, instance, created, **kwargs):
    if created:
        LeaveNotificationEmployee.objects.create(
            leave=instance.leave,
            user=instance.leave.employee,
            notification = "Your request for absence {} from {} to {} has been rejected by your supervisor / coordinator".format(instance.leave.leave_type, instance.leave.leave_date, instance.leave.return_date),
        )
        LeaveNotificationEmployee.objects.create(
            leave=instance.leave,
            user=instance.leave.employee.userprofile.boss.user,
            notification = "You rejected the request for absence {} from {} to {}.".format(instance.leave.leave_type, instance.leave.leave_date, instance.leave.return_date),
        )

post_save.connect(notification_reject_leave, sender=RejectLeave)


def notification_add_leave(sender, instance, created, **kwargs):
    if created:
        LeaveNotificationEmployee.objects.create(
            leave=instance,
            user=instance.employee,
            notification = "Request for absence {} from {} to {} has been added.".format(instance.leave_type, instance.leave_date, instance.return_date),
        )
        LeaveNotificationEmployee.objects.create(
            leave=instance,
            user=instance.employee.userprofile.boss.user,
            notification = "Employee {} {} send request for absence {} from {} to {}".format(instance.employee.first_name, instance.employee.last_name, instance.leave_type, instance.leave_date, instance.return_date),
        )

post_save.connect(notification_add_leave, sender=Leave)