from django.db import models
from django.contrib.auth.models import User


class Firm(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    nip = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Section(models.Model):
    
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class OnlyDirectorManager(models.Manager):
    def get_queryset(self):
        return super(OnlyDirectorManager, self).get_queryset().filter(user__groups__name='admin')


class OnlySupervisorManager(models.Manager):
    def get_queryset(self):
        return super(OnlySupervisorManager, self).get_queryset().filter(user__groups__name='supervisor')


class Boss(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, blank= True, on_delete=models.CASCADE)


    objects = models.Manager()
    only_director_role = OnlyDirectorManager()
    only_supervisor_role = OnlySupervisorManager()

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    
    boss = models.ForeignKey(Boss, null=True, on_delete=models.CASCADE)
    firm = models.ForeignKey(Firm, null=True, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.CASCADE)

    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=8, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    possition = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True)

    image = models.ImageField(default="profile_pic.png", null=True, blank=True, upload_to='profile')

    def __str__(self):
        return self.user.username


class BankInfo(models.Model):
    employee = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_number = models.CharField(max_length=28, null=True, blank=True)

    def __str__(self):
        return self.employee.username


class SalaryInfo(models.Model):
    employee = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    CONTRACT = (
        ('contract of employment', 'contract of employment'),
        ('contract work', 'contract work'),
        ('contract of mandate', 'contract of mandate'),
    )
    
    salary = models.IntegerField(null=True, blank=True)
    year_salary = models.IntegerField(null=True, blank=True)
    type_contract = models.CharField(max_length=100, null=True, blank=True, choices=CONTRACT)


    def __str__(self):
        return self.employee.first_name + " " + str(self.salary)