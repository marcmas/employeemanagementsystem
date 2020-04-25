from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import UserProfile, BankInfo, SalaryInfo
from django.contrib.auth.models import Group
from leave.models import VacationLimit
from django.shortcuts import redirect

def info_employee(sender, instance, created, **kwargs):
    if created:
        # group = Group.objects.get(name='employee')
        # instance.groups.add(group)

        UserProfile.objects.create(
            user = instance,
            )
        BankInfo.objects.create(
            employee = instance,
            )
        SalaryInfo.objects.create(
            employee = instance,
            )


post_save.connect(info_employee, sender=User)
