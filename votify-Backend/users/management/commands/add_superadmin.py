# users/management/commands/add_superadmin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        User = get_user_model()

        # Collecting email and password from user input
        email = input('Enter email address for the superuser: ').strip()
        if not email:
            self.stdout.write(self.style.ERROR(
                'Email address cannot be empty'))
            return

        password = input('Enter password for the superuser: ').strip()
        if not password:
            self.stdout.write(self.style.ERROR('Password cannot be empty'))
            return

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(
                'A user with this email already exists'))
            return

        # Create the superuser
        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
