import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
from faker import Faker
from elections.models import Election, Candidate


class Command(BaseCommand):
    help = 'Generate active elections for this week with candidate images'

    def handle(self, *args, **kwargs):
        fake = Faker()

        election_types = [
            Election.PRESIDENT,
            Election.VICE_PRESIDENT,
            Election.TREASURER,
            Election.PRO,
            Election.GENERAL_SECRETARY,
            Election.FINANCIAL_SECRETARY,
            Election.WELFARE_OFFICER,
            Election.ASSISTANT_GENERAL_SECRETARY
        ]

        departments = [
            'Marine Engineering',
            'Nautical Science',
            'Maritime Transport and Business Studies',
            'Computer Science',
            'Fisheries Technology',
            'Mechanical Engineering',
            'Science Laboratory Technology',
            'Industrial and Labour Relations',
            'Oceanography and Fisheries Science',
            'Hydrology and Water Resources Management',
            'MARITIME TRANSPORT AND BUSSINESS MANAGEMENT'
        ]

        school_levels = [
            Candidate.ND1,
            Candidate.ND2,
            Candidate.HNG1,
            Candidate.HNG2
        ]

        # Define today's date in Nigeria time (West Africa Time, UTC+1)
        nigeria_tz = timezone.get_fixed_timezone(60)  # 60 minutes = UTC+1
        today = timezone.now().astimezone(nigeria_tz).date()

        # Set the start and end of today in Nigeria time
        start_of_today = timezone.make_aware(
            datetime.combine(today, datetime.min.time()), nigeria_tz)
        end_of_today = timezone.make_aware(
            datetime.combine(today, datetime.max.time()), nigeria_tz)

        # Generate elections that start today
        for _ in range(5):  # Generate 5 active elections starting today
            start_date = fake.date_time_between(
                start_date=start_of_today, end_date=end_of_today, tzinfo=nigeria_tz)
            end_date = start_date + timedelta(days=random.randint(1, 3))

            election = Election.objects.create(
                election_type=random.choice(election_types),
                start_date=start_date,
                end_date=end_date,
                status='Active',
            )

            self.stdout.write(self.style.SUCCESS(
                f'Election {election.election_type} created: {start_date} to {end_date}'))

            # Generate sample candidates for each election
            for _ in range(random.randint(3, 8)):
                full_name = fake.name()
                department = random.choice(departments)
                school_level = random.choice(school_levels)
                matriculation_number = f"{fake.year(
                )}/{department[:4].upper()}/{school_level}/{fake.random_int(min=100, max=999)}"
                email = f"{full_name.split(' ')[0].lower()}.{
                    full_name.split(' ')[-1].lower()}@fcfmt.edu.ng"

                image_url = fake.image_url(width=640, height=480)

                candidate = Candidate.objects.create(
                    election=election,
                    full_name=full_name,
                    matriculation_number=matriculation_number,
                    department=department,
                    school_level=school_level,
                    about=fake.paragraph(nb_sentences=3),
                    manifesto=fake.paragraph(nb_sentences=5),
                    image=image_url,  # Add the image field here
                )

                self.stdout.write(self.style.SUCCESS(
                    f'Candidate {candidate.full_name} created for {election.election_type}'))
