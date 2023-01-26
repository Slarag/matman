from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from ..models import Material, UserProfile, Scheme


class TestBookmarking(TestCase):
    def setUp(self) -> None:
        self.scheme = Scheme.objects.create(name='dummy_scheme', description='dummy for testing',
                                            prefix='dummy-', numlen=6)
        self.material = Material.objects.create(scheme=self.scheme, short_text='dummy material')
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.profile1 = self.user1.profile
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.profile2 = self.user2.profile
        # login = self.client.login(username='testuser', password='12345')

    def test_bookmarking(self):
        self.assertFalse(self.profile1.has_bookmarked(self.material))
        self.assertFalse(self.profile2.has_bookmarked(self.material))

        self.profile1.bookmark(self.material)
        self.assertTrue(self.profile1.has_bookmarked(self.material))
        self.assertFalse(self.profile2.has_bookmarked(self.material))
        self.assertTrue(self.material.is_bookmarked_by_user(self.user1))
        self.assertFalse(self.material.is_bookmarked_by_user(self.user2))

        self.profile2.bookmark(self.material)
        self.assertTrue(self.profile1.has_bookmarked(self.material))
        self.assertTrue(self.profile2.has_bookmarked(self.material))
        self.assertTrue(self.material.is_bookmarked_by_user(self.user1))
        self.assertTrue(self.material.is_bookmarked_by_user(self.user2))

        self.profile1.unbookmark(self.material)
        self.assertFalse(self.profile1.has_bookmarked(self.material))
        self.assertTrue(self.profile2.has_bookmarked(self.material))
        self.assertFalse(self.material.is_bookmarked_by_user(self.user1))
        self.assertTrue(self.material.is_bookmarked_by_user(self.user2))

        self.profile2.unbookmark(self.material)
        self.assertFalse(self.profile1.has_bookmarked(self.material))
        self.assertFalse(self.profile2.has_bookmarked(self.material))
        self.assertFalse(self.material.is_bookmarked_by_user(self.user1))
        self.assertFalse(self.material.is_bookmarked_by_user(self.user2))

    def tearDown(self) -> None:
        self.scheme.delete()
        self.material.delete()
        self.user1.delete()
        self.user2.delete()
        self.profile1.delete()
        self.profile2.delete()
