from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class AuthAccountBackend(ModelBackend):
    """
    overriding authenticate method to use user's email instead of username for verifying credentials
    """

    def authenticate(self, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(user):
                return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None