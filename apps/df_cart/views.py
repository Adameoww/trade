from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

from .models import *
from df_user import user_decorator


@user_decorator.login
def user_cart(request):
    uid = request.session['user_id']
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    carts = CartInfo.objects.filter(user_id=uid)
    cart_num = CartInfo.objects.filter(user_id=uid).count()
    context = {
        'title': 'Shopping Cart',
        'page_name': 1,
        'guest_cart': 1,
        'carts': carts,
        'cart_num': cart_num,
        'user': user,
    }
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        # Get the total number of items the user has purchased
        return JsonResponse({'count': count})
    else:
        return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    uid = request.session['user_id']
    gid, count = int(gid), int(count)
    # Check if the item is already in the cart. If yes, update the quantity; if not, create a new entry.
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # If the request is via AJAX, return JSON; otherwise, redirect to the shopping cart page.
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        # Get the total number of items the user has purchased
        return JsonResponse({'count': count})
    else:
        return redirect(reverse("df_cart:cart"))


@user_decorator.login
def edit(request, cart_id, count):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        cart.save()
        data['count'] = 0
    except Exception:
        data['count'] = count
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data['ok'] = 1
    except Exception:
        data['ok'] = 0
    return JsonResponse(data)
