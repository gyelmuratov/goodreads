from django.contrib.auth import get_user
from users.models import CustomUser
from django.http import  response
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class RegisterTestCase(TestCase):
    def test_user_account_creation(self):
         self.client.post(
                    reverse('users:register'),
                          data ={
                                 'username': 'gulam',
                                 'first_name': 'gulam',
                                 'last_name': 'Yelmuratov',
                                 'email': 'gulamyelmuratov6@gmail.com',
                                 'password': 'Asd123/*-'
                          }
                          )
         user = CustomUser.objects.get(username='gulam')
         self.assertEqual(user.first_name, 'gulam')
         self.assertEqual(user.last_name, 'Yelmuratov')
         self.assertEqual(user.email, 'gulamyelmuratov6@gmail.com')
         self.assertNotEqual(user.password, 'Asd123/*-')
         self.assertTrue(user.check_password('Asd123/*-'))

    def test_required_fields(self):
         response=self.client.post(
                    reverse('users:register'),
             data = {
                 'first_name': 'gulam',
                 'email': 'gulamyelmuratov6@gmail.com',
             }
         )

         user_count = CustomUser.objects.count()
         self.assertEqual(user_count, 0)
         form = response.context['form']
         self.assertFormError(form, 'username', 'This field is required.')
         self.assertFormError(form, 'password', 'This field is required.')


    def test_invalid_email(self):
         response=self.client.post(
            reverse('users:register'),
             data={
                 'username': 'gulam',
                 'first_name': 'gulam',
                 'last_name': 'Yelmuratov',
                 'email': 'Invalid-email',
                 'password': 'Asd123/*-'
             }
         )
         user_count = CustomUser.objects.count()
         self.assertEqual(user_count, 0)
         form = response.context['form']

         self.assertFormError(form, 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = CustomUser.objects.create(username='gulam', first_name='gulam')  # Django ORM
        user.set_password('Asd123/*-')
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'gulam',
                'first_name': 'gulam',
                'last_name': 'Yelmuratov',
                'email': 'gulamyelmuratov6@gmail.com',
                'password': 'Asd123/*-'
            }
        )

        user_count = CustomUser.objects.count()

        form = response.context['form']

        self.assertFormError(
            form,
            'username',
            'A user with that username already exists.'
        )


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='gulam', first_name='gulam')
        self.db_user.set_password('Asd123/*-')
        self.db_user.save()
        # DRY DONT REPEAT YOURSELF

    def test_successful_login(self):

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'gulam',
                'password': 'Asd123/*-'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong_username',
                'password': 'Asd123/*-'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'gulam',
                'password': 'wrong-password'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):

        self.client.login(username='gulam', password='Asd123/*-')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login'))

    def test_profile_details(self):
        user = CustomUser.objects.create(username='gulam',
                                   first_name='gulam',
                                   last_name='Yelmuratov',
                                   email='gulamyelmuratov6@gmail.com')
        user.set_password('Asd123/*-')
        user.save()
        self.client.login(username='gulam', password='Asd123/*-')

        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(username='gulam',
                                   first_name='gulam',
                                   last_name='Yelmuratov',
                                   email='gulamyelmuratov6@gmail.com')
        user.set_password('Asd123/*-')
        user.save()
        self.client.login(username='gulam', password='Asd123/*-')
        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'username': 'gulam',
                'first_name': 'gulam',
                'last_name': 'Doe',
                'email': 'gulamyelmuratov5@gmail.com'
            }
        )
        #user = User.objects.get(pk=user.pk)
        user.refresh_from_db()

        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'gulamyelmuratov5@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))















