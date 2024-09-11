from django.contrib.auth import get_user_model
import logging
from .models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model 
from django.contrib.auth.backends import BaseBackend  # Add this import

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

'''

# Configure logging
logger = logging.getLogger(__name__)
'''

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug(f"Authenticating: username={username}, password={password}, kwargs={kwargs}")

        if username is None:
            username = kwargs.get('email')

        if username is None:
            # Correctly get matriculation number
            username = kwargs.get('matriculation_number')

        if username is None:
            logger.warning("No username or email provided for authentication.")
            return None

        try:
            user_model = get_user_model()
            if '@' in username:
                user = user_model.objects.get(email=username)
                logger.debug(f"Found user with email: {username}")
            else:
                user = user_model.objects.get(matriculation_number=username)
                logger.debug(
                    f"Found user with matriculation number: {username}")

            if user.check_password(password):
                logger.debug(f"Password matched for user: {user.email}")
                return user
            else:
                logger.warning(
                    f"Password did not match for user: {user.email}")
                return None
        except user_model.DoesNotExist:
            logger.error(f"User not found with username: {username}")
            return None
'''

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, matriculation_number=None, password=None):
        User = get_user_model()

        if username:
            # Handle email authentication for admins
            try:
                user = User.objects.get(email=username)
                if user.check_password(password) and user.user_type == 'admin':
                    logger.info(
                        f"Admin authentication successful for email: {username}")
                    return user
                else:
                    logger.warning(
                        f"Failed admin authentication attempt for email: {username}")
            except User.DoesNotExist:
                logger.warning(f"Admin user not found with email: {username}")

        if matriculation_number:
            # Handle matriculation number authentication for students
            try:
                user = User.objects.get(
                    matriculation_number=matriculation_number)
                if user.check_password(password) and user.user_type == 'student':
                    logger.info(f"Student authentication successful for matriculation number: { matriculation_number}")
                    return user
                else:
                    logger.warning(f"Failed student authentication attempt for matriculation number: {matriculation_number}")
            except User.DoesNotExist:
                logger.warning(f"Student user not found with matriculation number: { matriculation_number}")

        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            logger.info(f"Retrieved user with ID: {user_id}")
            return user
        except User.DoesNotExist:
            logger.warning(f"User not found with ID: {user_id}")
            return None
