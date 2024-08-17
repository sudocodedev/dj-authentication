from .models import OTP
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from . import helper
from src.middleware.my_middleware import get_cached_request, has_cached_request
from threading import Thread
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()

@receiver(post_save, sender = User)
def user_handler(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_superuser: pass
        else:
            OTP.objects.create(user=instance, otp_expires_at = timezone.now() + timezone.timedelta(minutes=5))
        
        otp = OTP.objects.filter(user=instance).last()

        try:
            if has_cached_request():
                request = get_cached_request()
        except:
            raise Exception("Request not found in the storage")

        data = {
            'user': instance,
            'uid': urlsafe_base64_encode(force_bytes(instance.id)),
            'otp': otp.token,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': get_current_site(request).domain,
        }

        print(data)

        # send_email_otp = Thread(target=helper.send_otp_mail, kwargs=data)
        # send_phone_otp = Thread(target=helper.send_otp_phone, kwargs=data)

        # send_email_otp.start()
        # send_phone_otp.start()
    



        