from django.test import TestCase
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse

from .models import FanArt
import os


class TestFanArtViews(TestCase):
    """ Test class for the FanArt views & approval flow """

    user_data = {
        'username': 'username',
        'password': 'password',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
    }

    fan_art_data = {
        'title': 'title',
        'description': 'description',
        'publish_date': date.today,
    }


    def test_fan_art_approval_flow(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_login(user)
        with open('author_site_project/static/img/logo.png', 'rb') as file_pointer:
            fan_art_data = dict(self.fan_art_data, image=file_pointer)
            response = self.client.post(reverse('add_fan_art'), fan_art_data)

        fan_art = FanArt.objects.get(user_profile=user.profile, title=fan_art_data['title'])

        # Testing newly added fan art defaults to not approved
        self.assertFalse(fan_art.is_approved)

        # Get all fan art, validate we get a page and that the
        # new unapproved art is NOT on it
        response = self.client.get(reverse('all_fan_art'))
        self.assertEqual(response.status_code, 200)
        page = response.context['fan_art']
        self.assertEqual(page.paginator.num_pages, 1)
        self.assertFalse(fan_art in page.object_list)

        # Get the users own fan art, validate we get a page and that
        # the user's unapproved art IS on it
        response = self.client.get(reverse('user_fan_art'))
        self.assertEqual(response.status_code, 200)
        page = response.context['user_fan_art']
        self.assertEqual(page.paginator.num_pages, 1)
        self.assertTrue(fan_art in page.object_list)

        fan_art.is_approved = True
        fan_art.save()

        # Get all fan art, validate we get a page and that the
        # new art IS now on it and is approved
        response = self.client.get(reverse('all_fan_art'))
        self.assertEqual(response.status_code, 200)
        page = response.context['fan_art']
        self.assertEqual(page.paginator.num_pages, 1)
        self.assertTrue(fan_art in page.object_list)

        # Editing the fan art, and verifying that it has returned to unapproved
        updated_fan_art_data = dict(self.fan_art_data, title='title2')
        self.client.post(reverse('edit_fan_art', args=[fan_art.id]), updated_fan_art_data)
        fan_art.refresh_from_db()
        self.assertFalse(fan_art.is_approved)
        self.assertEqual(fan_art.title, updated_fan_art_data['title'])


    def test_delete_fan_art_view(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_login(user)
        with open('author_site_project/static/img/logo.png', 'rb') as file_pointer:
            fan_art_data = dict(self.fan_art_data, image=file_pointer)
            response = self.client.post(reverse('add_fan_art'), fan_art_data)

        fan_art = FanArt.objects.get(user_profile=user.profile, title=fan_art_data['title'])

        # Testing that the delete fan art function deletes the art correctly
        self.client.post(reverse('delete_fan_art', args=[fan_art.id]))
        with self.assertRaises(FanArt.DoesNotExist):
            fan_art = FanArt.objects.get(user_profile=user.profile, title=fan_art_data['title'])


    def test_only_owner_can_edit_and_delete_fanart(self):
        user_owning_fanart = User.objects.create_user(**self.user_data)
        self.client.force_login(user_owning_fanart)
        with open('author_site_project/static/img/logo.png', 'rb') as file_pointer:
            fan_art_data = dict(self.fan_art_data, image=file_pointer)
            response = self.client.post(reverse('add_fan_art'), fan_art_data)

        fan_art = FanArt.objects.get(user_profile=user_owning_fanart.profile, title=fan_art_data['title'])

        # Switch to another user
        other_user_data = dict(self.user_data, username='otheruser')
        other_user = User.objects.create_user(**other_user_data)
        self.client.force_login(other_user)

        # Try to edit the fan art as another user
        updated_fan_art_data = dict(self.fan_art_data, title='title2')
        self.client.post(reverse('edit_fan_art', args=[fan_art.id]), updated_fan_art_data)

        # Verify that the title is unchanged
        fan_art.refresh_from_db()
        self.assertEqual(fan_art.title, self.fan_art_data['title'])

        # Try to delete the fan art as another user
        self.client.post(reverse('delete_fan_art', args=[fan_art.id]))

        # Verify that the fan art still exists in the DB
        fan_art.refresh_from_db()

