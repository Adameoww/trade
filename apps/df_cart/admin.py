from django.contrib import admin

from .models import CartInfo


@admin.register(CartInfo)
class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'count']
    list_per_page = 5
    list_filter = ['user', 'goods', 'count']
    search_fields = ['user__uname', 'goods__gtitle']#The issue is here: 'user' and 'goods' are ForeignKey fields, and need to be retrieved from the related ForeignKey table.
    readonly_fields = ['user', 'goods', 'count']