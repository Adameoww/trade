# -*- coding: utf-8 -*-
__date__ = '2019/5/1 20:09'


def goods_recommend(user):
    pass


def load_data_set(user):

    user_order_list = []
    for big_order in user.orderinfo_set.all():
        # Get all product IDs in this order
        user_little_order_list = [str(good.goods.id) for good in big_order.orderdetailinfo_set.all()]
        user_order_list.append(user_little_order_list)

    data_set = user_order_list
    return data_set
