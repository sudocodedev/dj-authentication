from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("signin/", views.user_signin, name="signin-page"),
    path("signout/", views.user_signout, name="signout-page"),
    path("edit/<int:accountID>/", views.account_edit, name="account-edit-page"),
    path("signup/", views.user_signup, name="signup-page"),
    path("verify-account/<uidb64>/", views.verify_account, name="verify-account"),
    path("resend-otp/", views.resend_otp, name="resend-otp"),
    path("password-reset/", views.password_reset, name="password-reset"),
    path("password-reset/<uidb64>/<token>/", views.password_reset_request, name="reset-request"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

