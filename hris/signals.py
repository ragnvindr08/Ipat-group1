# signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Employee

@receiver(post_save, sender=User)
def employee_profile(sender, instance, created, **kwargs):
    if created:
        group_name = kwargs.pop('group_name', None)
        if group_name:
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)

        Employee.objects.create(
            user=instance,
            first_name=instance.first_name,
            surname=instance.last_name,
        )
        
        
        print('Profile Created!')
