from django.contrib import admin

from .models import UserInfo, GoodsBrowser


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["uname", "usex", "uage", "upersonInf", "uemail", "ulogo", "ushou", "uaddress",
                    "uyoubian", "uphone", "urealname", "uzhengjian_type", "uzhengjian_tel",
                    "uzhengjian_img", "ucheck_passOrfail", "uname_passOrfail"]
    list_per_page = 5  # Number of items per page
    list_filter = ["uname", "uyoubian"]  # Filters for the list view
    search_fields = ["uname", "uyoubian"]  # Search fields
    readonly_fields = ["uname"]  # Fields that are read-only in the detail page
    # Editable fields in the list view
    # list_editable = ["ucheck_passOrfail"]


class GoodsBrowserAdmin(admin.ModelAdmin):
    list_display = ["user", "good"]
    list_per_page = 50  # Number of items per page
    list_filter = ["user__uname", "good__gtitle"]  # Filters for the list view
    search_fields = ["user__uname", "good__gtitle"]  # Search fields
    readonly_fields = ["user", "good"]  # Fields that are read-only in the detail page
    refresh_times = [3, 5]  # Auto-refresh intervals (in seconds)


# Set the admin panel header and title
admin.site.site_header = 'Second-hand Goods Trading Platform Admin System'
admin.site.site_title = 'Second-hand Goods Trading Platform Admin System'

# Register models with the admin site
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(GoodsBrowser, GoodsBrowserAdmin)
