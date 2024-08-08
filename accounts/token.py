from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    # Adds user.is_active as part of the token to be generated
    def _make_hash_value(self, user, timestamp) -> str:
        return (six.text_type(user.id) + six.text_type(timestamp) + six.text_type(user.is_active))
    
account_activation_token = AccountPasswordResetTokenGenerator()