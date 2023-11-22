import re

from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm as DjangoAuthForm
from django.contrib.auth import authenticate, login

from .models import User


class CustomDate(forms.DateInput):
    template_name = 'components/form/flatpickr_date.html'


class AuthenticationIdentifierForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}))

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Invalid Email format.")

        if not email:
            raise forms.ValidationError("Please provide an email address")

        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No user registered with this email address")

        return self.cleaned_data


class AuthenticationCompleteForm(forms.Form):
    password = forms.CharField(strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password.'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request

        super().__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data.get("password")
        email = self.request.session.get('user_email')

        if not password:
            raise forms.ValidationError("Please provide a password")

        if email is not None and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError("Incorrect Password")

            login(self.request, user)

        del self.request.session['user_email']

        return self.cleaned_data


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("password1", "password2",)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise forms.ValidationError("Please provide both password")

        if password1 != password2:
            raise forms.ValidationError("Both password doesn't match")

        return self.cleaned_data


class UserCreationNameForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if not first_name or not last_name:
            raise forms.ValidationError("Please provide your first name and last name")

        self.request.session['user'] = {
            'first_name': first_name,
            'last_name': last_name
        }

        return self.cleaned_data


class UserCreationBasicInfoForm(forms.ModelForm):
    birthday = forms.CharField(widget=CustomDate(attrs={'placeholder': 'Pick up a birth date'}))

    class Meta:
        model = User
        fields = ['birthday', 'gender']

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        birthday = self.cleaned_data.get('birthday')
        gender = self.cleaned_data.get('gender')

        if not birthday or not gender:
            raise forms.ValidationError("Please provide your birthday name and gender")

        user = self.request.session['user']
        self.request.session['user'] = {
            **user,
            'birthday': birthday,
            'gender': gender
        }

        return self.cleaned_data


class UserCreationEmailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}))

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError("Please provide your email address")

        user = self.request.session['user']
        self.request.session['user'] = {
            **user,
            'email': email,
        }

        return self.cleaned_data
