from django.urls import path
from .views import *

app_name = "documents"

urlpatterns = [
    path('add_regulation/', addRegulation, name='add_regulation'),
    path('view_list_regulations/', viewListRegulations, name="view_list_regulations"),
    path('<int:regulation_id>/detail_regulation/', viewDetailRegulation, name="view_detail_regulation"),
    path('view_list_regulations_user/', viewListRegulationsForUser, name="view_list_regulations_user"),
    path('<int:regulation_id>/detail_regulation_user/', viewDetailRegulationForUsers, name="view_detail_regulation_for_users"),
    path('<int:regulation_id>/accept_regulation/', acceptRegulation, name="accept_regulation"),
]

