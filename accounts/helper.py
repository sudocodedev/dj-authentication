import os
from django.core.mail import EmailMultiAlternatives
from django.utils import html
from django.template.loader import render_to_string
import requests
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from accounts.models import Notification


def login_sms_otp(**kwargs):
    
    notification = Notification.objects.create(user=kwargs.get('user'),
                                               action="signin-sms",
                                               message_type='info',
                                               status='pending',
                                               message= _("<i class='bx bx-info-square text-xl'></i> You will receive an SMS shortly if mobile no. is valid"))
    phone_number = kwargs.get('phonenumber')
    
    try:
        body = f"""
        𝐃𝐉 𝐂𝐑𝐔𝐃

        Hi,

        Your login OTP is {kwargs.get('otp')}.
        Do not share with anyone.
        Above OTP will expiry in 5 mins.
        """

        message = {
            "secret": os.environ.get('SMS_CHEF_API_KEY'),
            "mode": "devices",
            "device": os.environ.get("SMS_CHEF_DEVICE_ID"),
            "sim": 1,
            "priority": 1,
            "phone": phone_number,
            "message": body,
        }

        r = requests.post(url=os.environ.get("SMS_CHEF_URL"), params=message)

        if r.status_code == 200: 
            notification.status = 'success'
            notification.message_type = 'success'
            notification.message = _(f"<i class='bx bx-check-circle text-xl'></i> SMS sent to your mobile {phone_number} with login OTP")
        else:
            notification.status = 'failed'
            notification.message_type = 'error'
            notification.message = _(f"<i class='bx bx-error-circle text-xl'></i> Problem in sending SMS to {phone_number}")
    except Exception as e:
        notification.status = 'failed'
        notification.message_type = 'error'
        notification.message = _("<i class='bx bx-error-circle text-xl'></i> There is a server issue in sending SMS, Please try after sometime")
    
    notification.save()

def send_otp_phone(**kwargs):
    user = kwargs.get('user')
    phone_number = user.phonenumber.as_e164

    notification = Notification.objects.create(user=user,
                                               action='signup-sms',
                                               message_type='info',
                                               status='pending',
                                               message=_("<i class='bx bx-info-square text-xl'></i> You will receive an SMS shortly if mobile no. is valid")
                                               )

    try:
    
        body = f"""
        Hi {user.username} 👋

        Thanks for using 𝐃𝐉 𝐂𝐑𝐔𝐃,
        
        You have received this message because you have initiated account verification process in our site.

        Use the below OTP for account activation and it is valid only for ** 5 mins **:
            {kwargs.get('otp')[4:]}

        Read the instructions sent over mail clearly.
        For any queries, mail us to djauth@support.com. Our team will always be to help you out!

        Cheers,
        Team DJ CRUD
        """

        message = {
            "secret": os.environ.get('SMS_CHEF_API_KEY'),
            "mode": "devices",
            "device": os.environ.get("SMS_CHEF_DEVICE_ID"),
            "sim": 1,
            "priority": 1,
            "phone": phone_number,
            "message": body,
        }

        r = requests.post(url=os.environ.get("SMS_CHEF_URL"), params=message)

        if r.status_code == 200: 
            notification.status = 'success'
            notification.message_type = 'success'
            notification.message = _(f"<i class='bx bx-check-circle text-xl'></i> Account Verification SMS sent successfully to {phone_number}")
        else:
            notification.status = 'failed'
            notification.message_type = 'error'
            notification.message = _(f"<i class='bx bx-error-circle text-xl'></i> Problem in sending SMS to {phone_number}")

    except Exception as e:
        notification.status = 'failed'
        notification.message_type = 'error'
        notification.message = _("<i class='bx bx-error-circle text-xl'></i> There is a server issue in sending SMS, Please try after sometime")

    notification.save()

def send_otp_mail(**kwargs):
    
    notification = Notification.objects.create(user=kwargs.get('user'),
                                               action='signup-email',
                                               message_type='info',
                                               status='pending',
                                               message=_("<i class='bx bx-info-square text-xl'></i> You will receive an email shortly if the address is valid"))

    data = {
        "user": kwargs.get('user').username,
        "email": kwargs.get("user").email,
        "otp": kwargs.get("otp")[:4], # 1st 4 digits of OTP
        "uid": kwargs.get("uid"),
        "domain": kwargs.get("domain"),
        "protocol": kwargs.get("protocol")
    }

    try:
        html_message = render_to_string("accounts/email-verification.html", context=data)

        plain_message = html.strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="DJ CRUD: Account Verification | OTP",
            body=plain_message,
            to=[
                data.get("email"),
            ],
        )

        message.attach_alternative(html_message, "text/html")

        email_status = message.send()

        if email_status:
            notification.status = 'success'
            notification.message_type = 'success'
            notification.message = _(f"<i class='bx bx-check-circle text-xl'></i> Account Verification mail successfully sent to {data.get('email')}")
        else:
            notification.status = 'failed'
            notification.message_type = 'error'
            notification.message = _(f"<i class='bx bx-error-circle text-xl'></i> Problem in sending mail to {data.get('email')}, Double check once!")
    except Exception as e:
        notification.status = 'failed'
        notification.message_type = 'error'
        notification.message = _("<i class='bx bx-error-circle text-xl'></i> There is a server issue in sending mail, Please try after sometime")
    
    notification.save()


def send_password_reset(**kwargs):
    data = {
            'uid': kwargs.get('uid'),
            'user': kwargs.get('user').username,
            'token': kwargs.get('token'),
            'protocol': kwargs.get('protocol'),
            'domain': kwargs.get('domain'),
            'email': kwargs.get('user').email,
        }
    
    # Making an notification entry for password reset
    notification = Notification.objects.create(user=kwargs.get('user'), 
                                               action="forgot-pwd", 
                                               status="pending", 
                                               message_type='info',
                                               message= _("You will receive an email shortly if the address is valid."))
    try:
        
        html_message = render_to_string('accounts/pwd-reset-email.html', context=data)

        plain_message = html.strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject = "DJ CRUD: Password Reset Initiation",
            body=plain_message,  
            to=[data.get('email'),]
        )

        message.attach_alternative(html_message, "text/html")

        email_status = message.send()

        if email_status:
            notification.status = 'success'
            notification.message_type = 'success'
            notification.message = _(f"<i class='bx bx-check-circle text-xl'></i> Password reset mail sent successfully to {data.get('email')}")
        else:
            notification.status = 'failed'
            notification.message_type = 'error'
            notification.message = _(f"<i class='bx bx-error-circle text-xl'></i> Problem in sending mail to {data.get('email')}")
    
    except Exception as e:
        notification.status = 'failed'
        notification.message_type = 'error'
        notification.message = _("<i class='bx bx-error-circle text-xl'></i> There was a server issue, Please try after sometime")

    notification.save()
    
