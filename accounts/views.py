from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import SetPasswordForm
from .forms import AccountCreationForm, AccountLoginForm, AccountEditForm, AccountPwdResetForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import OTP, Notification
from . import helper
from .tokens import account_activation_token
from threading import Thread
from django.contrib.sites.shortcuts import get_current_site
import secrets
from django.conf import settings


User = get_user_model() # custom user model


######################## LOGIN ########################

def user_signin(request):
    print("inside login view")
    if request.method == 'POST':
        print("inside post req")
        form = AccountLoginForm(request, data=request.POST)
        if form.is_valid():
            print("inside form validation")
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)

            print("authentication -->", user)

            # if user:
            print("user has been authenticated")
            if User.objects.get(email=email).login_sms_otp:
                print("You are not supposed to be in this block")
                # Enabled Login OTP via SMS
                account = User.objects.get(email=email)
                otp = OTP.objects.create(
                                            user=account, 
                                            token=secrets.randbits(16),
                                            otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
                                        )
                # fetching User data
                uid = urlsafe_base64_encode(force_bytes(account.id))                
                data = {
                    'phonenumber': account.phonenumber.as_e164,
                    'otp': otp.token,
                    'user': account,
                }
                print(data)
                # Sending OTP
                send_login_otp = Thread(target=helper.login_sms_otp, kwargs=data)
                send_login_otp.start()
                # messages.info(request, _(f"SMS sent to your mobile {data.get('phonenumber')} with OTP"))
                return redirect("verify-login-otp", uid)
            else:
                # Default Login
                print("normal login")
                login(request, user)
                messages.success(request, _("User logged in"))
                return redirect('home-page')
        else:
            print("I'm here in last error part")
            messages.error(request, _("user credentials are not correct"))
            return render(request, 'accounts/authentication-page.html', { 'form': form, 'action': 'sigin' })
    else:
        form = AccountLoginForm()

    context = { 'form': form, 'action': 'sigin' }
    return render(request, 'accounts/authentication-page.html', context)

def verify_login_otp(request, uidb64):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)
    db_otp = OTP.objects.filter(user=user).last()
    print(f"DB OTP: {db_otp.token} | entered OTP: {request.POST.get('otp_code')}")

    if request.method == "POST":
        if request.POST.get('otp_code') == db_otp.token:
            if db_otp.otp_expires_at > timezone.now():
                login(request, user, backend='accounts.backend.AuthAccountBackend')
                messages.success(request, _("User logged in"))
                return redirect('home-page')
            else:
                messages.error(request, _("OTP got expired, Get a new one"))
                return redirect("verify-login-otp", uidb64)
        else:
            messages.error(request, _("Invalid OTP, Enter a valid one"))
            return redirect("verify-login-otp", uidb64)
    
    return render(request, 'accounts/verify_account.html', {'action': 'login', 'id': uidb64, 'user_id': uid, 'sitekey': settings.RECAPTCHA_PUBLIC_KEY})

def signin_status(request,userID):
    try:
        notification = Notification.objects.filter(user__id=userID, action="signin-sms").latest('created_at')

        return JsonResponse({'status': notification.status,
                             'type': notification.message_type,
                             'action': notification.action,
                             'message': notification.message}, safe=True)
    except:
        return JsonResponse({
            'status': "NA",
            'message': "No notifications found for this user"
        })


def resend_login_sms_otp(request, uidb64):
    uid = force_str(urlsafe_base64_decode(uidb64))
    account = User.objects.get(id=uid)
    otp = OTP.objects.create(
                                user=account, 
                                token=secrets.randbits(16),
                                otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
                            )
    # fetching User data                
    data = {
        'phonenumber': account.phonenumber.as_e164,
        'otp': otp.token,
        'user': account,
    }
    # Sending OTP
    send_login_otp = Thread(target=helper.login_sms_otp, kwargs=data)
    send_login_otp.start()
    return redirect("verify-login-otp", uidb64)


def user_signout(request):
    logout(request)
    messages.info(request, _("User logged out"))
    return redirect('home-page')


######################## END LOGIN ########################


######################## SIGN UP ########################

def user_signup(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username').lower()
            user.is_active = False
            user.save()
            print(user.id)
            messages.info(request, _("Account Verification process initiated"))
            return render(request, 'accounts/accounts.html', {'form': form, 'user_id': user.id})
        else:
            messages.error(request, _("Kindly check below errors"))
    else:
        form = AccountCreationForm()
    context = {'form': form}
    return render(request, 'accounts/accounts.html', context)

def verify_account(request, uidb64):
    # getting user & otp from the DB based on incoming request
    user_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=user_id)
    db_otp = OTP.objects.filter(user=user).last() # fetching lastest OTP table for request.user
    print(f"db otp : {db_otp.token} | entered otp: {request.POST.get('otp_code')}")

    if request.method == "POST":
        if request.POST.get('otp_code') == db_otp.token:
            if db_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, _("Your account has been verified successfully, Redirecting to Login page"))
                return redirect('signin-page')
            else:
                messages.error(request, _("OTP got expired, get a new OTP"))
                return redirect("verify-account", uidb64)
        else:
            messages.error(request, _("Invalid OTP has been entered, enter valid OTP"))
            return redirect("verify-account", uidb64)
    
    return render(request, 'accounts/verify_account.html')


def signup_status(request, userID):
    try:
        message = {}
        email = Notification.objects.filter(user__id=userID, action="signup-email").latest('created_at')
        sms = Notification.objects.filter(user__id=userID, action="signup-sms").latest('created_at')

        return JsonResponse({
            'key': 2,
            'email': {'status': email.status, 'action': email.action, 'type': email.message_type, 'message': email.message, },
            'sms': {'status': sms.status, 'action': sms.action, 'type': sms.message_type, 'message': sms.message, }
        })
    
    except Notification.DoesNotExist:
        return JsonResponse({
            'key': 1,
            'status': 'NA',
            'message': "No notifications found for this user"
        })


def resend_otp(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        phonenumber = request.POST.get("phonenumber")
        
        try:
            user = User.objects.get(email=email, phonenumber=phonenumber)
        except User.DoesNotExist:
            messages.error(request, _("Entered details didn't match with DB, Enter a valid one"))
            return redirect('resend-otp')
        
        # Generating a new OTP
        otp = OTP.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

        data = {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'otp': otp.token,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': get_current_site(request).domain,
        }

        print(data['user'].email, data['user'].phonenumber)
        send_email_otp = Thread(target = helper.send_otp_mail, kwargs=data)
        send_sms_otp = Thread(target = helper.send_otp_phone, kwargs=data)

        send_email_otp.start()
        send_sms_otp.start()

        messages.info(request, _("Account Verification process re-initiated"))
        return render(request, 'accounts/verify_account.html', {'action': 'resend', 'user_id': user.id, 'sitekey': settings.RECAPTCHA_PUBLIC_KEY})

    context={'action': 'resend', 'sitekey': settings.RECAPTCHA_PUBLIC_KEY}
    return render(request, 'accounts/verify_account.html', context)

######################## END SIGN UP ########################


######################## FORGOT Password ########################


def password_reset(request):

    user_id = ''
    if request.method == "POST":
        form = AccountPwdResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            user_id = user.id
            data = {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
                'domain': get_current_site(request).domain,
                'protocol': 'https' if request.is_secure() else 'http',
            }
            
            reset_email = Thread(target=helper.send_password_reset, kwargs=data)
            reset_email.start()

            messages.info(request, _("Password Reset process initiated"))
            return render(request, 'accounts/authentication-page.html', {'form': form, 'action': 'forgot', 'user_id': user_id})
        else:
            # for rendering form field errors
            return render(request, 'accounts/authentication-page.html', {'form': form, 'action': 'forgot'})
    else:
        form = AccountPwdResetForm()

    context = {'action': 'forgot', 'form': form, 'user_id': user_id}
    return render(request, 'accounts/authentication-page.html', context)


def password_reset_status(request, userID):
    try:
        notification = Notification.objects.filter(user__id=userID).latest('created_at')

        return JsonResponse({'status': notification.status,
                             'type': notification.message_type,
                             'action': notification.action,
                             'message': notification.message}, safe=True)
    except:
        return JsonResponse({
            'status': "NA",
            'message': "No notifications found for this user"
        })


def password_reset_request(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                user.refresh_from_db()
                user.save()
                messages.success(request, _("New password has been set successfully, You can login now"))
                return redirect('signin-page')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
    
        form = SetPasswordForm(user)
        context = {'action': "setpwd",'form': form, 'sitekey': settings.RECAPTCHA_PUBLIC_KEY}
        return render(request, 'accounts/authentication-page.html', context)
    
    else:
        messages.error(request, _("Password Reset verification link has been expired, redirecting to Password Reset page"))
        return redirect('password-reset')

######################## END FORGOT Password ########################


######################## User Reset Password ########################

def account_reset_password(request, accountID):
    user = User.objects.get(id=accountID)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.refresh_from_db()
            user.save()
            messages.success(request, _('Password changed successfully!'))
            return redirect('account-view-page',user.id)
        
    form = SetPasswordForm(user)
    context = {'action': 'setpwd', 'form': form, 'sitekey': settings.RECAPTCHA_PUBLIC_KEY}
    return render(request, 'accounts/authentication-page.html', context)


######################## END User Reset Password ########################


######################## PROFILE ########################

def account_view(request, accountID):
    try:
        account = User.objects.get(id=accountID)
    except User.DoesNotExist:
        messages.error(request, _("User doesn't exist, redirecting to home page"))
        return redirect('home-page')
    return render(request, 'accounts/view-account.html', {'account':account})         


def account_edit(request, accountID):
    try:
        account = User.objects.get(id=accountID)
    except User.DoesNotExist:
        messages.error(request, _("User doesn't exist, redirecting to home page"))
        return redirect('home-page')
    
    if request.method == 'POST':
        form = AccountEditForm(request.POST, instance = request.user)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username').lower()
            user.email = form.cleaned_data.get('email').lower()
            user.save()
            messages.success(request, _("Account updated successfully"))
            return redirect('home-page')
        else:
            messages.error(request, _("Kindly check below errors"))
    else:
        form = AccountEditForm(instance=request.user)

    context = {'form': form, 'action': 'edit'}
    return render(request, 'accounts/accounts.html', context)

######################## END PROFILE ########################