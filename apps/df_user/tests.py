from django.test import TestCase, Client
from django.urls import reverse
from df_user.models import UserInfo

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserInfo.objects.create(
            uname="testuser",
            upwd="testpass",
            uemail="test@example.com"
        )
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    def test_info_page(self):
        response = self.client.get(reverse("df_user:info"))
        self.assertEqual(response.status_code, 200)
