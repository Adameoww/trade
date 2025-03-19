from datetime import datetime

from django.db import models
from tinymce.models import HTMLField  # Using a rich text editor requires installation in the settings file

# Maintain the one-to-many relationship within GoodsInfo. 
# Additionally, both product information and category information are important and should use logical deletion.


class TypeInfo(models.Model):
    # Product category information (e.g., Fruits, Seafood, etc.)
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="Category")

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    # Specific product information
    isDelete = models.BooleanField(default=False)  # Logical deletion
    gtitle = models.CharField(max_length=20, verbose_name="Product Name", unique=True)
    gpic = models.ImageField(verbose_name='Product Image', upload_to='df_goods/image/%Y/%m', null=True, blank=True)  # Product image
    gprice = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Product Price")  # Price with two decimal places
    gunit = models.CharField(max_length=20, verbose_name="Seller Nickname")
    gclick = models.IntegerField(verbose_name="Click Count", default=0, null=False)
    gjianjie = models.CharField(max_length=200, verbose_name="Description")
    gkucun = models.IntegerField(verbose_name="Stock", default=0)
    gcontent = HTMLField(max_length=200, verbose_name="Details")
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, verbose_name="Category")  # Foreign key to TypeInfo

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.gtitle


class GoodsContent(models.Model):
    # User comments
    isDelete = models.BooleanField(default=False)  # Logical deletion
    ctitle = models.CharField(max_length=20, verbose_name="Product Name")
    cpic = models.ImageField(verbose_name='Uploaded Image', upload_to='df_goods/image/%Y/%m', null=True, blank=True)  # Uploaded image
    cusername = models.CharField(max_length=20, verbose_name="Buyer Nickname")
    clogo = models.CharField(verbose_name='Buyer Avatar', max_length=200, default=None)
    cuser_content = HTMLField(max_length=200, verbose_name="User Comment")
    date_publish = models.DateTimeField(verbose_name="Published Date", default=datetime.now)
    cgoodsname = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Related Product")  # Foreign key to GoodsInfo

    class Meta:
        verbose_name = "Product Comment"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ctitle


class ContentChart(models.Model):
    # Comment replies
    isDelete = models.BooleanField(default=False)  # Logical deletion
    ctitle = models.CharField(max_length=20, verbose_name="Product Name")
    cusername = models.CharField(max_length=20, verbose_name="Commenter Nickname")
    cusername1 = models.CharField(max_length=20, verbose_name="Replier Nickname")
    ccontent_chart = HTMLField(max_length=200, verbose_name="Comment Reply")
    date_publish = models.DateTimeField(verbose_name="Published Date", default=datetime.now)
    ccontent = models.ForeignKey(GoodsContent, on_delete=models.CASCADE, verbose_name="Comment ID")  # Foreign key to GoodsContent

    class Meta:
        verbose_name = "Comment Reply"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ctitle
