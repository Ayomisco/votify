from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        User = get_user_model()

        # Collecting email, full name, and password from user input
        email = input('Enter email address for the superuser: ').strip()
        if not email:
            self.stdout.write(self.style.ERROR(
                'Email address cannot be empty'))
            return

        full_name = input('Enter full name for the superuser: ').strip()
        if not full_name:
            self.stdout.write(self.style.ERROR('Full name cannot be empty'))
            return

        password = input('Enter password for the superuser: ').strip()
        if not password:
            self.stdout.write(self.style.ERROR('Password cannot be empty'))
            return

        # Ensure the email is unique
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(
                'A user with this email already exists'))
            return

        # Create the superuser
        User.objects.create_superuser(
            email=email,
            password=password,
            full_name=full_name,
            user_type='admin'  # Ensure this is set to admin for superuser
        )
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
