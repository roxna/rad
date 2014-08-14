from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase
from bills.forms import RegistrationForm
from bills.models import User

# Create your tests here.


class FormTestCase(TestCase):
    def test_clean_username(self):
        form = RegistrationForm()
        form.cleaned_data = {'username': 'test-user'}
        self.assertEqual(form.cleaned_data['username'], 'test-user')

    def test_clean_username_exception(self):
        User.objects.create_user(username='test-user')
        form = RegistrationForm()
        form.cleaned_data = {'username': 'test-user'}
        # Use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()


class ViewTestCase(TestCase):
    def create_user(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)

    def test_register_page(self):
        data = {
            'username': self.username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)

        # Check this user was created in the database
        self.assertTrue(User.objects.filter(username=self.username).exists())

        # Check it's a redirect to the dashboard page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('dashboard')))

    def test_login_page(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(reverse('login'), data)

        # Check it's a redirect to the dashboard page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('dashboard')))