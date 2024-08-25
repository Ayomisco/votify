from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from users.models import User


class Command(BaseCommand):
    help = 'Delete users by their email addresses permanently'

    def handle(self, *args, **options):
        emails = self.prompt_for_emails()
        deleted_count = 0
        not_found_count = 0

        for email in emails:
            try:
                user = User.objects.get(email=email)
                user.delete()  # Permanently deletes the user
                deleted_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully deleted user: {email}'))
            except ObjectDoesNotExist:
                not_found_count += 1
                self.stdout.write(self.style.ERROR(
                    f'User with email {email} does not exist'))

        self.stdout.write(self.style.SUCCESS(
            f'Total users deleted: {deleted_count}'))
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(
                f'Total users not found: {not_found_count}'))

    def prompt_for_emails(self):
        emails = []
        while True:
            email = input(
                "Enter an email address to delete (or type 'done' to finish): ").strip()
            if email.lower() == 'done':
                break
            if email:
                emails.append(email)
            else:
                self.stdout.write(self.style.WARNING(
                    "Email cannot be empty. Please enter a valid email address."))
        return emails
