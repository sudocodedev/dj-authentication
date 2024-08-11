from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import secrets

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "user_otp")
    token = models.CharField(max_length=8, default = secrets.token_hex(4))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"

class AccountUserManager(BaseUserManager):
    # creating user function
    def create_user(self, email, username, password=None):
        # validating params
        if not email:
            raise ValueError(_("user must have an email address"))
        if not username:
            raise ValueError(_("user must have a username"))

        # account creation
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # creating a super user
    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class UserAccount(AbstractUser):
    email = models.EmailField(
        max_length=160,
        verbose_name=_("Email Address"),
        unique=True,
        blank=False,
        null=True,
    )
    username = models.CharField(
        max_length=50, verbose_name=_("User Name"), blank=False, null=False
    )
    avatar = models.ImageField(upload_to="profile_images/")
    phonenumber = PhoneNumberField(blank=True)
    login_sms_otp = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ("username",)

    objects = AccountUserManager()

    def __str__(self):
        return self.username

