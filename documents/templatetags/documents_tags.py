from django import template
from documents.models import RegulationsStatus

register = template.Library()

@register.simple_tag
def unread_regulations(request):
    user = request.user
    return RegulationsStatus.has_noaccept_regulation.filter(employee=user).count()