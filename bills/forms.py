from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from bills.models import User

__author__ = 'roxnairani'


class RegistrationForm(UserCreationForm):
        name = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Full Name',
                                   'name': 'name',
                                   'class': 'form-control'
                               }))
        username = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'Username',
                                       'name': 'username',
                                       'class': 'form-control'
                                   }))
        email = forms.EmailField(required=True,
                                 widget=forms.EmailInput(attrs={
                                     'placeholder': 'E-mail',
                                     'name': 'email',
                                     'class': 'form-control'
                                 }))
        password1 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Password',
                                        'name': 'password1',
                                        'class': 'form-control'
                                    }))
        password2 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Confirm Password',
                                        'name': 'password2',
                                        'class': 'form-control'
                                    }))
        image = forms.ImageField(required=False)

        class Meta:
            model = User
            fields = ("name", "username", "email", "password1", "password2", "image")

        def clean_username(self):
            username = self.cleaned_data["username"]
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )


class LoginForm(AuthenticationForm):
        username = forms.CharField(max_length=254,
                                   required=True,
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'Username',
                                       'class': 'form-control'
                                   }))
        password = forms.CharField(required=True,
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': 'Password',
                                       'class': 'form-control'
                                   }))


class ProfileForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Full Name',
                                'class': 'form-control'
                           }))
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Username',
                                   'class': 'form-control'
                               }))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'E-mail',
                                 'class': 'form-control'
                             }))
    # image = forms.ImageField(required=True,
    #                          widget=forms.FileInput)

    class Meta:
        model = User
        fields = ['name', 'username', 'email']


class UploadDataForm(forms.Form):
    # file is a reserved python keyword
    file = forms.FileField(required=True)
    password = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Password',
                                   'class': 'form-control' }))
