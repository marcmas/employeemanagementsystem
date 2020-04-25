from django.contrib import admin
from .models import Leave, VacationLimit, AcceptLeave, RejectLeave, LeaveNotificationEmployee


admin.site.register(Leave)
admin.site.register(VacationLimit)
admin.site.register(AcceptLeave)
admin.site.register(RejectLeave)
admin.site.register(LeaveNotificationEmployee)
