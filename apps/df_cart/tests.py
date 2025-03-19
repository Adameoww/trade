from django.test import TestCase, Client
from django.urls import reverse
from df_goods.models import GoodsInfo, TypeInfo
from df_cart.models import CartInfo
from df_user.models import UserInfo
class CartTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = UserInfo.objects.create(
            uname="testuser",
            upwd="testpass",
            uemail="testuser@example.com"
        )

        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

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

    def test_cart_page_loads(self):
        response = self.client.get(reverse('df_cart:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'df_cart/cart.html')

    def test_add_to_cart(self):
        response = self.client.post(reverse('df_cart:add', args=[self.goods.id, 2]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CartInfo.objects.filter(user=self.user, goods=self.goods).exists())  # 确保购物车有该商品

        json_data = response.json()
        self.assertIn('count', json_data)

    def test_edit_cart_item(self):
        self.client.post(reverse('df_cart:add', args=[self.goods.id, 2]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # 先添加商品
        cart_item = CartInfo.objects.get(user=self.user, goods=self.goods)

        response = self.client.post(reverse('df_cart:edit', args=[cart_item.id, 5]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        cart_item.refresh_from_db()
        self.assertEqual(cart_item.count, 5)

    def test_delete_cart_item(self):
        self.client.post(reverse('df_cart:add', args=[self.goods.id, 2]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # 先添加商品
        cart_item = CartInfo.objects.get(user=self.user, goods=self.goods)

        response = self.client.post(reverse('df_cart:delete', args=[cart_item.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        self.assertFalse(CartInfo.objects.filter(user=self.user, goods=self.goods).exists())  # 确保商品被删除

        json_data = response.json()
        self.assertEqual(json_data['ok'], 1)
