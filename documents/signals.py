from django.db.models.signals import post_save, m2m_changed
from .models import Regulations, RegulationsStatus
from django.contrib.auth.models import User

def create_regulation_status_for_employee(sender, instance, action, **kwargs):
    if action == "post_add":
        regulations = instance.employee.through.objects.filter(regulations_id=instance.id)
        for regulation in regulations:
            print(regulation)
            RegulationsStatus.objects.create(
                employee = User.objects.get(id=regulation.user_id),
                regulation = Regulations.objects.get(id=regulation.regulations_id)
            )


m2m_changed.connect(create_regulation_status_for_employee, sender=Regulations.employee.through)