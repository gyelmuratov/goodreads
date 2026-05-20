from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTest(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='111111')
        user = CustomUser.objects.create(username='gulam',
                                         first_name='gulam',
                                         last_name='Yelmuratov',
                                         email='gulamyelmuratov6@gmail.com')
        user.set_password('Asd123/*-')
        user.save()

        review1=BookReview.objects.create(book=book, user=user, stars_given=3, comment="Very good book")
        review2=BookReview.objects.create(book=book, user=user, stars_given=4, comment="Useful book")
        review3=BookReview.objects.create(book=book, user=user, stars_given=5, comment="Nice book")

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review3.comment)  # Nice book - 1-sahifa
        self.assertContains(response, review2.comment)  # Useful book - 1-sahifa
        self.assertNotContains(response, review1.comment)  # Very good book - 2-sahifada


