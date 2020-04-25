from django.contrib import admin
from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views


app_name = "user"

urlpatterns = [
    path('', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('users/', users, name='users'),
    path('add_user/', addEmployeePage, name='add_user'),

    path('<int:user_id>/view_user_info/', viewUser, name='view_user_info'),

    path('<int:user_id>/delete_user/', deleteUserPage, name='delete_user'),

    path('<int:user_id>/update_base_info/', updateBaseInfoPage, name='update_base_info'),
    path('<int:user_id>/update_userprofile_info/', updateUserprofileInfoPage, name='update_userprofile_info'),
    path('<int:user_id>/update_salaryinfo_info/', updateSalaryInfoPage, name='update_salaryinfo_info'),
    path('<int:user_id>/update_bankinfo_info/', updateBankInfoPage, name='update_bankinfo_info'),
    path('<int:user_id>/set_new_password/', downloadUserPassword, name='set_new_password'),
    path('<int:user_id>/update_profile_picture/', updateProfilePicturePage, name='update_profile_picture'),


    path('user_info/', infoUser, name='info_user'),
    path('settings_page/', settingsPage, name='settings_page'),
    path('activity_log/', activityPage, name='activity_log'),

    # Change password
    path('change_password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('user:password_change_done')), name='password_change'),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Change username
    path('change_username/', changeUsername, name="change_username"),
]
