#!/user/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'df_cart'

urlpatterns = [
    url(r'^$', views.user_cart, name="cart"),  # User cart page
    url(r'^add(\d+)_(\d+)/$', views.add, name="add"),  # Add item to cart
    url(r'^edit(\d+)_(\d+)/$', views.edit, name="edit"),  # Edit item in cart
    url(r'^delete(\d+)/$', views.delete, name="delete"),  # Delete item from cart
]
