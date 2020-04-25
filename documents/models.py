from django.db import models
from django.contrib.auth.models import User


class Regulations(models.Model):
    employee = models.ManyToManyField(User)

    description = models.CharField(max_length=300, null=False, blank=False)
    necessary = models.BooleanField(default=False)
    come_into_force = models.DateField()
    file = models.FileField(upload_to='regulations')

    def __str__(self):
        return str(self.description)

    def get_detail_url(self):
        return '/{}/detail_regulation'.format(self.id)

    def get_regulation_file_url(self):
        return "/images/{}".format(self.file)


class HasNoAcceptedRegulations(models.Manager):
    def get_queryset(self):
        return super(HasNoAcceptedRegulations, self).get_queryset().filter(accept=False)


class HasNoAcceptedNecessaryRegulations(models.Manager):
    def get_queryset(self):
        return super(HasNoAcceptedNecessaryRegulations, self).get_queryset().filter(accept=False).filter(regulation__necessary=True)


class RegulationsStatus(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    regulation = models.ForeignKey(Regulations, on_delete=models.CASCADE)

    accept = models.BooleanField(default=False)
    accept_date = models.DateField(null=True, blank=True)

    objects = models.Manager()
    has_noaccept_regulation = HasNoAcceptedRegulations()
    has_noaccept_necessary_regulation = HasNoAcceptedNecessaryRegulations()


    def __str__(self):
        return str(self.employee.username) + str(self.regulation.description)

    def get_detail_url(self):
        return '/{}/detail_regulation_user'.format(self.regulation.id)

    def get_regulation_file_url(self):
        return "/images/{}".format(self.regulation.file)

    def get_accept_regulation_url(self):
        return '/{}/accept_regulation'.format(self.regulation.id)


