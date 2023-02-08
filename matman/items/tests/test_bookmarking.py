from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from ..models import Item, UserProfile, Scheme


class TestBookmarking(TestCase):
    def setUp(self) -> None:
        self.scheme = Scheme.objects.create(name='dummy_scheme', description='dummy for testing',
                                            prefix='dummy-', numlen=6)
        self.item = Item.objects.create(scheme=self.scheme, short_text='dummy item')
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.profile1 = self.user1.profile
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.profile2 = self.user2.profile
        # login = self.client.login(username='testuser', password='12345')

    def test_bookmarking(self):
        self.assertFalse(self.profile1.has_bookmarked(self.item))
        self.assertFalse(self.profile2.has_bookmarked(self.item))

        self.profile1.bookmark(self.item)
        self.assertTrue(self.profile1.has_bookmarked(self.item))
        self.assertFalse(self.profile2.has_bookmarked(self.item))
        self.assertTrue(self.item.is_bookmarked_by_user(self.user1))
        self.assertFalse(self.item.is_bookmarked_by_user(self.user2))

        self.profile2.bookmark(self.item)
        self.assertTrue(self.profile1.has_bookmarked(self.item))
        self.assertTrue(self.profile2.has_bookmarked(self.item))
        self.assertTrue(self.item.is_bookmarked_by_user(self.user1))
        self.assertTrue(self.item.is_bookmarked_by_user(self.user2))

        self.profile1.unbookmark(self.item)
        self.assertFalse(self.profile1.has_bookmarked(self.item))
        self.assertTrue(self.profile2.has_bookmarked(self.item))
        self.assertFalse(self.item.is_bookmarked_by_user(self.user1))
        self.assertTrue(self.item.is_bookmarked_by_user(self.user2))

        self.profile2.unbookmark(self.item)
        self.assertFalse(self.profile1.has_bookmarked(self.item))
        self.assertFalse(self.profile2.has_bookmarked(self.item))
        self.assertFalse(self.item.is_bookmarked_by_user(self.user1))
        self.assertFalse(self.item.is_bookmarked_by_user(self.user2))

    def tearDown(self) -> None:
        self.scheme.delete()
        self.item.delete()
        self.user1.delete()
        self.user2.delete()
        self.profile1.delete()
        self.profile2.delete()
