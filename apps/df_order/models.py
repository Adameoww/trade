from django.db import models
from datetime import datetime

from df_goods.models import GoodsInfo
from df_user.models import UserInfo

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True, verbose_name="Main Order Number")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="Order User")
    odate = models.DateTimeField(auto_now=True, verbose_name="Date")
    oIsPay = models.BooleanField(default=False, verbose_name="Payment Status")
    ototal = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total Price")
    oaddress = models.CharField(max_length=150, verbose_name="Order Address")

    class Meta:
        verbose_name = "Unpaid Order"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}'s order on {1}".format(self.user.uname, self.odate)


class OrderDetailInfo(models.Model):

    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Product")
    username = models.CharField(max_length=20, verbose_name="Buyer Nickname", default=None)
    shopername = models.CharField(max_length=20, verbose_name="Seller Nickname", default="")
    datatime = models.DateTimeField(verbose_name="Transaction Time", default=datetime.now)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="Order")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Product Price")
    count = models.IntegerField(verbose_name="Product Quantity")

    class Meta:
        verbose_name = "Paid Order"
        verbose_name_plural = verbose_name

    def __str__(self):

        return "{0} (Quantity: {1})".format(self.goods.gtitle, self.count)
