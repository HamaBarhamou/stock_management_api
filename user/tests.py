from django.test import TestCase
from user.models import User


# Create your tests here.
class UserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            username = 'homo'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.username, 'homo')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        
#python manage.py test
