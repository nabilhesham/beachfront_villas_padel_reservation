from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates users'

    def handle(self, *args, **kwargs):
        # # delete all users
        # User.objects.all().delete()

        # generate default user list
        users = [{"username": "user_1", "password": "user_1"}, {"username": "user_2", "password": "user_2"},
                 {"username": "user_3", "password": "user_3"}]
        for villa_no in range(1, 192):
            users.append({"username": f"villa_{villa_no}", "password": f"villa_{villa_no}@123"})

        # create default users
        for user_obj in users:
            user, created = User.objects.get_or_create(username=user_obj['username'])
            if created:
                # Set the default password
                user.set_password(user_obj['password'])  # Set password
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User {user_obj["username"]} created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'User {user_obj["username"]} already exists'))

        # Create the admin user with admin privileges
        admin_username = "admin"
        admin_password = "admin"
        admin, created = User.objects.get_or_create(username=admin_username)
        if created:
            # Set a default password for the admin
            admin.set_password(admin_password)
            admin.default_password = False
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user {admin_username} created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin user {admin_username} already exists'))
