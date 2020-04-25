from .models import LeaveNotificationEmployee
from django.db.models import Q

def get_notifications(request):

    user = request.user

    if user.groups.filter(name='supervisor') or user.groups.filter(name='employee') or user.groups.filter(name='admin'):
        notifications_all = LeaveNotificationEmployee.objects.filter(Q(user=request.user) & Q(read=False)).count()
        notifications = LeaveNotificationEmployee.objects.filter(user=request.user).order_by('-date_created')[:4]

        return {'notifications': notifications, 'notifications_all': notifications_all}

    else:
        notifications = {}
        return {'notifications': notifications}

