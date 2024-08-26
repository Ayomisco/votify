from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model 

User = get_user_model()


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
