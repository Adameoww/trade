from django.db import models

from datetime import datetime
from tinymce.models import HTMLField

from df_goods.models import GoodsInfo



class UserInfo(models.Model):

    uname = models.CharField(max_length=20, verbose_name="Username", unique=True)
    usex = models.CharField(max_length=10, verbose_name="Gender", default="")
    uage = models.CharField(max_length=10, verbose_name="Age", default="")
    upersonInf = models.CharField(max_length=200, verbose_name="Personal Introduction", default="")
    ulogo= models.FileField(verbose_name="User Avatar",upload_to='images', default='default.jpg')
    upwd = models.CharField(max_length=40, verbose_name="User Password", blank=False)
    uemail = models.EmailField(verbose_name="Email", unique=True)
    urealname = models.CharField(max_length=20, default="", verbose_name="Real Name")
    uzhengjian_type = models.CharField(max_length=20, default="", verbose_name="ID Type")
    uzhengjian_tel = models.CharField(max_length=18, default="", verbose_name="ID Number")
    uzhengjian_img = models.FileField(upload_to='images/zhengjian_img', default="", verbose_name="ID Image")
    ucheck_passOrfail=models.BooleanField(verbose_name="Verification Approval", default=False)
    ushou = models.CharField(max_length=20, default="", verbose_name="Recipient Name")
    uaddress = models.CharField(max_length=100, default="", verbose_name="Address")
    uyoubian = models.CharField(max_length=6, default="", verbose_name="Postal Code")
    uphone = models.CharField(max_length=11, default="", verbose_name="Phone Number")
    uname_passOrfail = models.BooleanField(verbose_name="Allow Login", default=True)

    class Meta:
        verbose_name = "User Information"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.uname


class GoodsBrowser(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="User ID")
    good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Product ID")
    browser_time = models.DateTimeField(default=datetime.now, verbose_name="Browsing Time")

    class Meta:
        verbose_name = "User Browsing History"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0} viewed {1}".format(self.user.uname, self.good.gtitle)


class Information(models.Model):
    isDelete = models.BooleanField(default=False)
    ctitle = models.CharField(max_length=20, verbose_name="Product Name")
    cusername = models.CharField(max_length=20, verbose_name="Buyer Nickname")
    cusername1 = models.CharField(max_length=20, verbose_name="Seller Nickname")
    ccontent_chart = HTMLField(max_length=200, verbose_name="Message Content")
    ccheck = models.BooleanField(verbose_name="Message Read Status", default=False)
    date_publish = models.DateTimeField(verbose_name="Published Time", default=datetime.now)
    cinformation = models.ForeignKey(UserInfo, on_delete=models.CASCADE,
                                     verbose_name="Message")  # Foreign key linking to GoodsContent table

    class Meta:
        verbose_name = "User Messages"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cusername1


class tuihuoInfo(models.Model):
    isDelete = models.BooleanField(default=False)
    title = models.CharField(max_length=20, verbose_name="Product Name")
    username = models.CharField(max_length=20, verbose_name="Recipient Name")
    username1 = models.CharField(max_length=20, verbose_name="Sender Name")
    person_number = models.CharField(max_length=20, verbose_name="ID Card Number")
    order_number = models.CharField(max_length=20, verbose_name="Order Number")
    kuaidi = models.CharField(max_length=20, verbose_name="Courier Type")
    kuaidi_number = models.CharField(max_length=20, verbose_name="Courier Tracking Number")
    address = models.CharField(max_length=50, verbose_name="Shipping Address", default=None)
    address1 = models.CharField(max_length=50, verbose_name="Sender Address", default=None)
    text = HTMLField(max_length=200, verbose_name="Return Reason", default=None)
    passOrdefault = models.BooleanField(verbose_name="Refund Approved", default=False)
    date_publish = models.DateTimeField(verbose_name="Published Time", default=datetime.now)

    class Meta:
        verbose_name = "Return Orders"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
