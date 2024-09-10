from .models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model 

User = get_user_model()

'''
class MatricNumberBackend(ModelBackend):
    def authenticate(self, request, matriculation_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(matriculation_number=matriculation_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
'''


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Print for debugging
        print(f"Authenticating: username={username}, kwargs={kwargs}")

        # Check if username is None, fallback to kwargs for email
        if username is None:
            username = kwargs.get('email')  # Extract email from kwargs

        # Ensure username is not None before checking for '@'
        if username is None:
            print("No username or email provided for authentication.")
            return None

        try:
            if '@' in username:
                user = User.objects.get(email=username)
                print(f"Found user with email: {username}")
            else:
                user = User.objects.get(matriculation_number=username)
                print(f"Found user with matriculation number: {username}")

            if user.check_password(password):
                print(f"Password matched for user: {user.email}")
                return user
            else:
                print(f"Password did not match for user: {user.email}")
                return None
        except User.DoesNotExist:
            print(f"User not found with username: {username}")
            return None
