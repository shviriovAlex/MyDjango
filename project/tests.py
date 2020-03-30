from unittest import mock

from django.test import TestCase, Client

from project import models


class URLTests(TestCase):
    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_all_news(self):
        response = self.client.get('/all_news/')
        self.assertEqual(response.status_code, 200)

    def test_login_google(self):
        response = self.client.get('/oauth/login/google-oauth2/')
        self.assertEqual(response.status_code, 302)

    def test_login_git(self):
        response = self.client.get('/oauth/login/github/')
        self.assertEqual(response.status_code, 302)


class MaterialTestCase(TestCase):

    def setUp(self):
        super(MaterialTestCase, self).__init__()
        self.client = Client()
        self.user = models.User(first_name='alex')
        self.user.save()

    # def test_slug_created(self, expected_slug):
    #     """test slug={} created correctly"""
    #     response = self.client.post('/create/',
    #                                 {"title": expected_slug,
    #                                  "body": 'mybody',
    #                                  "status": 'private'})
    #     mat = models.NewsGame.objects.get()
    #     self.assertEqual(mat.slug, expected_slug)
    #
    # def test_slug_created_correctly(self, title, expected_slug):
    #     """test slug={} created correctly"""
    #     response = self.client.post('/create/',
    #                                 {"title": title,
    #                                  "body": 'mybody',
    #                                  "status": 'private'})
    #     mat = models.NewsGame.objects.get()
    #     self.assertEqual(mat.slug, expected_slug)
    #
    # def test_send_mail(self):
    #     mat = models.NewsGame(slug='slug',
    #                           author=self.user,
    #                           body='mybody')
    #     mat.save()
    #     with mock.patch('lesson.views.send_mail') as mail_mock:
    #         response = self.client.post('/' + str(mat.id) + '/share/',
    #                                     {"name": "name",
    #                                      "my_email": "dd@dd.ru",
    #                                      "to": "addr@dd.ru",
    #                                      "comment": "adsfadsf"})
    #     mail_mock.assert_called_once()
    #
    # def test_send_mail_args(self, mail_mock):
    #     mat = models.NewsGame(slug='slug',
    #                           author=self.user,
    #                           body='mybody')
    #     mat.save()
    #
    #     response = self.client.post('/' + str(mat.id) + '/share/',
    #                                 {"name": "name",
    #                                  "my_email": "dd@dd.ru",
    #                                  "to": "addr@dd.ru",
    #                                  "comment": "adsfadsf"})
    #     mail_mock.assert_called_once()
    #     mail_mock.assert_called_with()
