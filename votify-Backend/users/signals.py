from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import User
from .helpers.emails import Signup_confirmation


@receiver(post_save, sender=User)
def send_welcome_mail(instance, created, **kwargs):
    if created:
        # Add this line for tracking
        print("Signal triggered for user:", instance.matriculation_number)

        # Load the email template and render with context
        if 'student' in instance.user_type:
            body = render_to_string('emails/auth/student_welcome_email.html', {
                'full_name': instance.full_name.title()
            })
            Signup_confirmation(
                email=instance.email,
                event="user_sign_up",
                subject="Welcome to FCFMT Voting System",
                body=body
            )
            print(f"Signup email sent to student { instance.matriculation_number}")

        elif 'admin' in instance.user_type:
            body = render_to_string('emails/auth/admin_welcome_email.html', { 'full_name': instance.full_name
            })
            Signup_confirmation(
                email=instance.email,
                event="admin_sign_up",
                subject="Welcome Admin to FCFMT Voting System",
                body=body
            )
            print(f"Signup email sent to admin {instance.email}")

        # Notify the system owner/admin that a new user signed up
        notify_body = render_to_string('emails/auth/new_user_notification.html', {
            'full_name': instance.full_name.title(),
            'matriculation_number': instance.matriculation_number if 'student' in instance.user_type else 'N/A',
            'email': instance.email,
            'user_type': instance.user_type
        })

        admin_email = "mayokun.ishola@fcfmt.edu.ng"  # Replace with your admin email
        Signup_confirmation(
            email=admin_email,
            event="notify_user_signup",
            subject="New User Signup Notification",
            body=notify_body
        )
        print(f"Admin notified about the new signup: {instance.full_name}")
