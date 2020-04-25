from django import template
from django.contrib.auth.models import Group 


register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False


@register.filter(name='has_groups') 
def has_groups(user, group_name):
    group_name = group_name.strip(" ")
    group_name = group_name.split(',')
    for g in group_name:
        group = Group.objects.get(name=g)
        if group in user.groups.all():
            return True


@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return field.as_widget(attrs=attrs)