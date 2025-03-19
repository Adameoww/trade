from django.contrib import admin

from .models import OrderDetailInfo, OrderInfo
from df_user.models import tuihuoInfo


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ["oid", "user", "odate", "ototal", "oaddress"]
    list_per_page = 5
    list_filter = ["user", "odate", "oaddress"]
    search_fields = ["user__uname"]
    ordering = ["-odate"]


@admin.register(OrderDetailInfo)
class OrderDetailInfoAdmin(admin.ModelAdmin):

    list_display = ["goods", "order", "price", "count"]
    list_per_page = 5
    list_filter = ["goods"]

@admin.register(tuihuoInfo)
class tuihuoInfoAdmin(admin.ModelAdmin):
    list_display = ["title", "username", "username1", "person_number", "order_number","kuaidi","kuaidi_number","address","address1","text","passOrdefault","date_publish"]

    list_per_page = 5
    list_filter = ["title", "username", "username1","order_number"]
    search_fields = ["username"]
    ordering = ["-order_number"]