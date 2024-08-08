from django import forms
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField

User = get_user_model() # custom user model 

class AccountLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': "Enter mail address"}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': "Enter password"}))


class AccountPwdResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(AccountPwdResetForm, self).__init__(*args, **kwargs)
    email = forms.CharField(widget=TextInput(attrs={'placeholder': "Enter mail address"}))
    captcha = ReCaptchaField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Entered mail ID doesn't exists, Enter a valid one"))
        return email

class AccountCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'email', 'phonenumber')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Enter username"}),
            'email': forms.TextInput(attrs={'placeholder': "example@sample.com"}),
            'phonenumber': forms.TextInput(attrs={'placeholder': "9876543210"}),
            'first_name': forms.TextInput(attrs={'placeholder': "John"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Cruse"}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': "Type password"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': "Re-type password"})


    def name_checker(self, s1:str) -> int:
        # this fn check whether the input string has any numbers, special characters or not
        check = set('1234567890!@#$%^&*')
        return len(set(s1).intersection(check))

    def username_checker(self, s1:str) -> int:
        # this fn check whether the input string has any numbers, underscore & hypens or not
        check = set('1234567890_-')
        return len(set(s1).intersection(check))

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError(_('email already exists, try different one'))

        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError(_('username already exists, try different one'))

        if self.username_checker(username) == 0:
            raise forms.ValidationError(_('username should atleast contain numbers or hypen or an underscore'))

        return username

    def clean_first_name(self):
        f_name = self.cleaned_data['first_name']

        if self.name_checker(f_name):
            raise forms.ValidationError(_('first name should contain only letters'))

        return f_name

    def clean_last_name(self):
        check = set('1234567890!@#$%^&*')
        f_name, l_name = self.cleaned_data['first_name'], self.cleaned_data['last_name']

        if self.name_checker(l_name) > 0: 
            raise forms.ValidationError(_('last name should contain only letters'))

        if f_name == l_name:
            raise forms.ValidationError(_("first name can't be same as last name"))

        return l_name

    def clean_avatar(self):
        file = self.cleaned_data['avatar']
        file_suffix = file.name.split('.')[-1]
        file_size = file.size
        
        if file_suffix not in settings.DATA_UPLOAD_FILE_SUFFIX:
            raise forms.ValidationError(_("upload image with these extensions ➡ *.png, *.jpeg, *.jpg, *.gif"))
        
        if file_size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
            raise forms.ValidationError(_("upload image with atmost 3MB in size"))

        return file

    
class AccountEditForm(UserChangeForm):
    password = None # to prevent password field rendering in the browser
    
    class Meta:
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'email', 'phonenumber')
        exclude = ('password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Enter username"}),
            'email': forms.TextInput(attrs={'placeholder': "Eg. example@sample.com"}),
            'phonenumber': forms.TextInput(attrs={'placeholder': "Eg. 9876543210"}),
            'first_name': forms.TextInput(attrs={'placeholder': "John"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Cruse"}),
        }

    def __init__(self, *args, **kwargs):
        super(AccountEditForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(_('email already exists, try different one'))
        
        return email