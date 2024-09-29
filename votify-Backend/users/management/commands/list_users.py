from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'List all users ordered by registration date (created_at)'

    def handle(self, *args, **options):
        # Fetch all users ordered by created_at (registration date)
        users = User.objects.all().order_by('created_at')

        if users.exists():
            self.stdout.write(self.style.SUCCESS(
                "Listing all users ordered by registration date:\n"))
            for idx, user in enumerate(users, start=1):
                self.stdout.write(
                    f"{idx}. {user.first_name} - {user.email} (Registered on: {user.created_at})")
        else:
            self.stdout.write(self.style.ERROR(
                "No users found in the database."))
