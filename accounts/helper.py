import os
from django.core.mail import EmailMultiAlternatives
from django.utils import html
from django.template.loader import render_to_string
import requests
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def send_otp_phone(request, kwargs):
    API_KEY = os.environ.get('SMS_CHEF_API_KEY')

    phone_number = kwargs.get('phone')

    body = f"""
    Hi {kwargs.get('user')} 👋

    Thanks for using 𝐃𝐉 𝐂𝐑𝐔𝐃,
     
    You have received this message because you have initiated account verification process in our site.

    Use the below OTP for account activation:
        {kwargs.get('otp')[4:]}

    Read the instructions sent over mail clearly.
    For any queries, mail us to abc@xyz.com. Our team will always be to help you out!

    Cheers,
    Team DJ CRUD
    """

    message = {
        "secret": API_KEY,
        "mode": "devices",
        "device": os.environ.get("SMS_CHEF_DEVICE_ID"),
        "sim": 1,
        "priority": 1,
        "phone": phone_number,
        "message": body,
    }

    r = requests.post(url=os.environ.get("SMS_CHEF_URL"), params=message)

    if r.status_code == 200: 
        messages.success(request, _(f"OTP has been sent to your phonenumber <b>{phone_number}</b>"))
    else:
        messages.success(request, _(f"Problem in sending OTP to <b>{phone_number}</b>"))

def send_otp_mail(request, kwargs):
    data = {
        "user": kwargs.get('user'),
        "email": kwargs.get("email"),
        "otp": kwargs.get("otp"), #[:4], # 1st 4 digits of OTP
        "uid": kwargs.get("uid"),
        "domain": kwargs.get("domain"),
        "protocol": kwargs.get("protocol")
    }

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
        messages.success(
            request, _(f"OTP has been sent to <b>{data.get('email')}</b>")
        )
    else:
        messages.error(
            request, _(f"Problem in sending mail to <b>{data.get('email')}</b>")
        )


def send_password_reset(request, kwargs):
    
    data = {
        'uid': kwargs.get('uid'),
        'user': kwargs.get('user'),
        'token': kwargs.get('token'),
        'protocol': kwargs.get('protocol'),
        'domain': kwargs.get('domain'),
        'email': kwargs.get('email'),
    }
    
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
        messages.success(
            request, _("You have initiated password reset process successfully, You can close this browser window!")
        )
    else:
        messages.error(
            request, _(f"Problem in sending mail to <b>{data.get('email')}</b>")
        )

