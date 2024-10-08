from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create Manager group and assign permissions"

    def handle(self, *args, **kwargs):
        manager_group, created = Group.objects.get_or_create(name="Manager")

        permissions_to_add = [
            "add_customuser",
            "change_customuser",
            "delete_customuser",
            "view_customuser",
            "add_dish",
            "change_dish",
            "delete_dish",
            "view_dish",
            "add_dishreview",
            "change_dishreview",
            "delete_dishreview",
            "view_dishreview",
            "add_driver",
            "change_driver",
            "delete_driver",
            "view_driver",
        ]

        for perm_codename in permissions_to_add:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                manager_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Permission {perm_codename} does not exist.")
                )

        self.stdout.write(self.style.SUCCESS(f"Manager group created: {created}."))
        self.stdout.write(
            self.style.SUCCESS(
                f"Assigned permissions: {[perm.codename for perm in manager_group.permissions.all()]}"
            )
        )
