from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from users.models import User


class Command(BaseCommand):
    help = 'Delete users by their email addresses permanently'

    def add_arguments(self, parser):
        parser.add_argument(
            'emails',
            nargs='+',
            type=str,
            help='List of email addresses of users to delete'
        )

    def handle(self, *args, **options):
        emails = options['emails']
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
