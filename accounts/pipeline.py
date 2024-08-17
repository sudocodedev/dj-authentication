from social_core.exceptions import AuthAlreadyAssociated
from django.contrib.auth import get_user_model



def link_to_existing_user(backend, uid, user=None, *args, **kwargs):
    if user: return

    # Fetching User model
    User = get_user_model()
    email = kwargs.get('details').get('email')

    if email:
        try:
            existing_user = User.objects.get(email=email)
            #linking the social account to the next pipeline
            return {'user': existing_user} 
        except User.DoesNotExist:
            pass
    else:
        raise AuthAlreadyAssociated(backend, "the account is already associated with another user")


