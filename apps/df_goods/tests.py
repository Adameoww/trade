from django.test import TestCase, Client
from df_user.models import UserInfo
from df_goods.models import GoodsInfo, TypeInfo, GoodsContent
from django.urls import reverse

class GoodsTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user, created = UserInfo.objects.get_or_create(
            uname="testuser",
            defaults={"upwd": "testpass", "uemail": "test@example.com"}
        )
        self.client.session['user_id'] = self.user.id
        self.client.session.save()

        self.type = TypeInfo.objects.create(ttitle="Electronics")

        self.goods = GoodsInfo.objects.create(
            gtitle="Test Product",
            gprice=100.0,
            gunit="Seller001",
            gclick=0,
            gjianjie="A test product",
            gkucun=10,
            gcontent="Product details",
            gtype=self.type
        )

        self.comment = GoodsContent.objects.create(
            ctitle=self.goods.gtitle,
            cusername="testbuyer",
            cuser_content="Great product!",
            cgoodsname=self.goods,
            clogo="default_avatar.jpg"
        )

    def test_good_list_page(self):
        response = self.client.get(f'/list{self.type.id}_1_1/')
        self.assertEqual(response.status_code, 200)

    def test_good_detail_page(self):
        response = self.client.get(f'/detail/{self.goods.id}/')
        self.assertEqual(response.status_code, 200)

    def test_search_function(self):
        response = self.client.get(f'/search/?q={self.goods.gtitle}')
        self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        new_comment = GoodsContent.objects.create(
            ctitle="Another Comment",
            cusername="user2",
            cuser_content="Not bad",
            cgoodsname=self.goods,
            clogo="default_avatar.jpg"
        )
        self.assertEqual(GoodsContent.objects.count(), 2)
        self.assertEqual(new_comment.cusername, "user2")
