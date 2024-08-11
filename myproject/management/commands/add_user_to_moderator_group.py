from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Add user with id=1 to the "Модераторы" group and assign permissions'

    def handle(self, *args, **kwargs):
        permissions_ids = [30, 32, 34, 36]
        group_name = 'Модераторы'
        group, created = Group.objects.get_or_create(name=group_name)
        for perm_id in permissions_ids:
            try:
                permission = Permission.objects.get(id=perm_id)
                if not group.permissions.filter(id=perm_id).exists():
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'Permission {perm_id} added to the "{group_name}" group.'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {perm_id} does not exist.'))
        try:
            user = User.objects.get(id=1)
            if user.groups.filter(name=group_name).exists():
                self.stdout.write(self.style.SUCCESS(f'User with id=1 is already in the "{group_name}" group.'))
            else:
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'User with id=1 has been added to the "{group_name}" group.'))
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR('User with id=1 does not exist.'))
