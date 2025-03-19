from django.db import models

from df_user.models import UserInfo
from df_goods.models import GoodsInfo

# When there is a one-to-many relationship, such as fresh food categories and specific fresh food items,
# the relationship is maintained in the "many" table, meaning it is maintained in the specific product table.
# For many-to-many relationships, a new table should be created to maintain the relationships.

# The relationship between the user table and the product table is maintained in the shopping cart table.

# Logical deletion vs. physical deletion in the shopping cart: Choose physical deletion.
# The items in the shopping cart are not considered important data, so they can be deleted directly.

class CartInfo(models.Model):

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="User")
    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="Product")
    count = models.IntegerField(verbose_name="", default=0)  # Records how many units of a product the user buys

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.uname + "'s Shopping Cart"
