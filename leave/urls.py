from django.urls import path
from .views import *

app_name = "leave"

urlpatterns = [
    # Dashboards
    path('dashboard/', dashboard, name='dashboard'),

    # Json leave
    path('json_pending_leave/', jsonPendingLeave, name='json_pending_leave'),
    path('json_accepted_leave/', jsonAcceptedLeave, name='json_accepted_leave'),
    path('json_rejected_leave/', jsonRejectedLeave, name='json_rejected_leave'),

    path('calendar/', calendar, name='calendar'),

    # Export xls  
    path('export_leave_xls/', export_leave_xls, name='export_leave_xls'),
    path('export_employyes_leaves_xls/', export_employyes_leaves_xls, name='export_employyes_leaves_xls'),
    path('export_employyes_limits_xls/', export_employyes_limits_xls, name='export_employyes_limits_xls'),

    # Leaves
    path('add_leave', addLeave, name='add_leave'),
    path('list_leaves', listLeaves, name='list_leaves'),
    path('view_vacation_limits', detailVacationLimits, name='view_vacation_limits'),

    # Leaves view
    path('view_pending_leaves', viewPendingLeaves, name='view_pending_leaves'),
    path('view_accepted_leaves', viewAcceptedLeaves, name='view_accepted_leaves'),
    path('view_rejected_leaves', viewRejectedLeaves, name='view_rejected_leaves'),

    # Notifications
    path('notifications/', viewNotifications, name='view_notifications'),
    path('<int:notification_id>/accept_notifications/', acceptNotification, name='accept_notifications'),

    # Leaves action
    path('<int:leave_id>/detail_leave', detailLeave, name='detail_leave'),
    path('<int:leave_id>/accept_leave', acceptLeave, name='accept_leave'),
    path('<int:leave_id>/reject_leave', rejectLeave, name='reject_leave'),
    path('<int:user_id>/update_vacation_limits', updateVacationLimitPage, name='update_vacation_limits'),

    # Leave limits
    path('view_employees_limits', viewListEmployeesLimits, name='view_list_employees_limits'),
    path('<int:employee_id>/view_employees_limits', viewEmployeesLimits, name='view_employees_limits')

]
