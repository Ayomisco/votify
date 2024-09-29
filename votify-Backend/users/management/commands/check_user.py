from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Check if a user exists by email in the database'

    def handle(self, *args, **options):
        email = input("Email:\n>>>> ").lower()

        # Check if a user with the provided email exists
        user = User.objects.filter(email=email).first()
        if user is None:
            self.stdout.write(self.style.ERROR(
                f"User with email '{email}' does not exist"))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"User with email '{email}' exists"))
