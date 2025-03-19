import uuid
from random import Random

from django.shortcuts import render,render_to_response
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse

from hashlib import sha1

from django.contrib import messages

import df_goods
from df_goods.models import TypeInfo,GoodsInfo,GoodsContent,ContentChart
from df_cart.models import CartInfo
from .models import GoodsBrowser,UserInfo,Information,tuihuoInfo
from . import user_decorator
from df_order.models import *

from django.core.mail import send_mail


def register(request):

    context = {
        'title': 'User Registration',
    }
    return render(request, 'df_user/register.html', context)


def register_handle(request):

    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    confirm_pwd = request.POST.get('confirm_pwd')
    email = request.POST.get('email')

    # Check password consistency
    if password != confirm_pwd:
        return redirect('/user/register/')
    # Encrypt password
    s1 = sha1()
    s1.update(password.encode('utf8'))
    encrypted_pwd = s1.hexdigest()

    # Create user object
    UserInfo.objects.create(uname=username, upwd=encrypted_pwd, uemail=email)
    # Registration successful
    context = {
        'title': 'User Login',
        'username': username,
    }
    return render(request, 'df_user/login.html', context)


def register_exist(request):
    username = request.GET.get('uname')
    uemail = request.GET.get('uemail')
    count = UserInfo.objects.filter(uname=username).count()
    email_count = UserInfo.objects.filter(uemail=uemail).count()
    print(email_count)
    return JsonResponse({'count': count, 'email_count': email_count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': 'User Login',
        'error_name': 0,
        'error_pwd': 0,
        'error_vc': 0,
        'uname': uname,
    }
    return render(request, 'df_user/login.html', context)


# Captcha display
def verify_show(request):
    return render(request, 'df_user/login.html')


def login_handle(request):

    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    jizhu = request.POST.get('jizhu', 0)
    vc = request.POST.get('vc')
    verifycode = request.session['verifycode']
    user = UserInfo.objects.filter(uname=uname)
    print("user:%s" % (user))
    if len(user) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == user[0].upwd and vc == verifycode and user[0].uname_passOrfail == True:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return red
        elif s1.hexdigest() == user[0].upwd and vc != verifycode:
            context = {
                'title': 'User Login',
                'error_name': 0,
                'error_pwd': 0,
                'error_vc': 1,
                'uname': uname,
                'upwd': upwd,
                'user': user,
                'vc': vc,
            }
            return render(request, 'df_user/login.html', context)
        elif user[0].uname_passOrfail == False:
            messages.success(request, "Your account has been banned due to violations.")
            context = {
                'title': 'User Login',
                'uname': uname,
                'upwd': upwd,
                'user': user,
                'vc': vc,
            }
            return render(request, 'df_user/login.html', context)
        else:
            context = {
                'title': 'User Login',
                'error_name': 0,
                'error_pwd': 1,
                'error_vc': 1,
                'uname': uname,
                'upwd': upwd,
                'user': user,
                'vc': vc,
            }
            return render(request, 'df_user/login.html', context)
    else:
        context = {
            'title': 'User Login',
            'error_name': 1,
            'error_pwd': 0,
            'error_vc': 0,
            'uname': uname,
            'upwd': upwd,
            'user': user,
            'vc': vc,
        }
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect(reverse("df_goods:index"))


def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def findpwdView(request):
    context = {
        'title': 'Reset Password',
    }
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        print("username:%s" % (username))
        user = UserInfo.objects.get(uname=username)
        context = {
            'title': 'Reset Password',
            'user': user,
        }
        if user.uemail == email:
            email_title = "Second-Hand Goods Trading Platform - Password Reset"
            code = random_str()
            request.session["code"] = code
            email_body = "Your password has been reset. For account security, do not share your password. Your new password is: {0}".format(code)
            send_status = send_mail(email_title, email_body, 'admin@example.com', [email], fail_silently=False)
            code = request.session["code"]
            s1 = sha1()
            s1.update(code.encode('utf8'))
            encrypted_pwd = s1.hexdigest()
            user.upwd = encrypted_pwd
            user.save()
            del request.session["code"]
            messages.success(request, "Password has been reset. Please check your email.")
        else:
            messages.success(request, "User email does not match the entered email. Reset failed.")

        return render(request, "df_user/change_password1.html", context)
    return render(request, "df_user/change_password1.html", context)


@user_decorator.login
def info(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
    cart_num = CartInfo.objects.filter(user_id=int(uid)).count()
    goods_list = []
    if browser_goods:
        goods_list = [browser_good.good for browser_good in browser_goods]
        explain = 'Recently Viewed'
    else:
        explain = 'No Recent Views'

    context = {
        'title': 'User Center',
        'page_name': 1,
        'guest_cart': 1,
        'cart_num': cart_num,
        'user_phone': user.uphone,
        'user_address': user.uaddress,
        'user_name': user.uname,
        'user': user,
        'ucheck_passOrfail': user.ucheck_passOrfail,
        'goods_list': goods_list,
        'explain': explain,
    }
    return render(request, 'df_user/user_center_info.html', context)



@user_decorator.login
def order(request, index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
    cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()
    tuohuo_infos = tuihuoInfo.objects.filter()
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    user = UserInfo.objects.get(id=request.session['user_id'])
    context = {
        'paginator': paginator,
        'page': page,
        # 'orders_list':orders_list,
        'title': "User Center",
        'user':user,
        'page_name': 1,
        'guest_cart': 1,
        'cart_num':cart_num,
        'tuohuo_infos':tuohuo_infos,
    }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    cart_num = CartInfo.objects.filter(user_id=user.id).count()
    if request.method == "POST":
        user.ushou = request.POST.get('ushou')
        user.uaddress = request.POST.get('uaddress')
        user.uyoubian = request.POST.get('uyoubian')
        user.uphone = request.POST.get('uphone')
        user.save()
    context = {
        'page_name': 1,
        'title': 'User Center',
        'user': user,
        'guest_cart': 1,
        'cart_num':cart_num,
    }
    return render(request, 'df_user/user_center_site.html', context)

@user_decorator.login
def publishers(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    cart_num = CartInfo.objects.filter(user_id=user.id).count()
    typeinfos = TypeInfo.objects.all()
    if request.method == "POST":
        gtitle = request.POST.get('title')
        gpic = request.FILES.get('pic')
        gunit = user.uname
        gprice = request.POST.get('price')
        gjianjie = request.POST.get('jianjie')
        gkucun = request.POST.get('kucun')
        gcontent = request.POST.get('content')
        gtype_id = request.POST.get('type_id')
        if gtitle == "" or gpic == "" or gprice == "" or gjianjie == "" or gkucun == "" or gcontent == "":
            messages.success(request, "Please complete all required fields!")
        elif int(gprice) >= 100000:
            messages.success(request, "Price cannot exceed 100000!")
        else:
            GoodsInfo.objects.create(gtitle=gtitle, gpic=gpic, gunit=gunit, gprice=gprice, gjianjie=gjianjie, gkucun=gkucun, gcontent=gcontent, gtype_id=gtype_id)
            messages.success(request, "Product published successfully!")

    context = {
        'page_name': 1,
        'title': 'User Center',
        'user': user,
        'typeinfos': typeinfos,
        'guest_cart': 1,
        'cart_num': cart_num,
    }
    return render(request, 'df_user/user_publishers.html', context)

@user_decorator.login
def changeInformation(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    cart_num = CartInfo.objects.filter(user_id=user.id).count()
    #users = UserInfo.objects.filter()
    context = {
        'page_name': 1,
        'title': 'User Center',
        'user': user,
        'guest_cart': 1,
        'cart_num': cart_num,
    }
    # if request.method == "GET":
    #     page_id=str(uuid.uuid4())
    #     request.session["pageid"]=page_id
    #     return render(request, 'df_user/user_changeInformation.html', {'pageid':page_id})

    if request.method == "POST":
        logo = request.FILES.get('logo')
        if logo:
            user.ulogo = logo
        else:
            user.ulogo = user.ulogo

        user.usex = request.POST.get('sex')
        user.uage = request.POST.get('age')
        user.upersonInf = request.POST.get('personinf')
        user.save()
    return render(request, 'df_user/user_changeInformation.html', context)

@user_decorator.login
def changeInPwd(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    cart_num = CartInfo.objects.filter(user_id=user.id).count()
    #users = UserInfo.objects.filter()
    context = {
        'page_name': 1,
        'title': 'User Center',
        'user': user,
        'guest_cart': 1,
        'cart_num': cart_num,
    }
    # if request.method == "GET":
    #     page_id=str(uuid.uuid4())
    #     request.session["pageid"]=page_id
    #     return render(request, 'df_user/user_changeInformation.html', {'pageid':page_id})

    if request.method == "POST":
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == "" or password2 == "":
            messages.success(request, "Please enter the password you want to change!")
        elif password == password2:
            s1 = sha1()
            s1.update(password.encode('utf8'))
            encrypted_pwd = s1.hexdigest()
            user.upwd = encrypted_pwd
            user.save()
            messages.success(request, "Password changed successfully!")
        else:
            messages.success(request, "The two entered passwords do not match!")
    return render(request, 'df_user/user_changePwd.html', context)


@user_decorator.login
def check_user(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    cart_num = CartInfo.objects.filter(user_id=user.id).count()
    if request.method == "POST":
        user.urealname = request.POST.get('name')
        user.uzhengjian_type = request.POST.get('type_id')
        user.uzhengjian_tel = request.POST.get('tel')
        user.uzhengjian_img = request.FILES.get('pic')
        if user.urealname == None or user.uzhengjian_type == None or user.uzhengjian_tel == None or user.uzhengjian_img == None:
            print("error: Please complete all required fields")
            messages.success(request, "Please complete all required fields")
        else:
            user.save()
            print("Please wait for approval")
            messages.success(request, "Submission successful, please wait for approval")

    context = {
        'page_name': 1,
        'title': 'User Center',
        'user': user,
        'guest_cart': 1,
        'cart_num': cart_num,
    }
    return render(request, 'df_user/user_check_username.html', context)


def shoper_information(request, cname):
    shoper = UserInfo.objects.get(uname=cname)
    content_username = cname
    Content = GoodsContent.objects.get(cusername=content_username)

    goods = GoodsInfo.objects.filter(gunit=content_username)

    orderinfs = OrderDetailInfo.objects.filter(shopername=cname).order_by('-datatime')
    infors = GoodsInfo.objects.filter()

    if 'user_id' in request.session:
        uid = request.session['user_id']
        user = UserInfo.objects.get(id=uid)
        if request.method == "POST":
            ctitle = request.POST.get('title')
            cusername = user.uname
            cusername1 = content_username
            ccontent_chart = request.POST.get('Message')
            cinformation_id = shoper.id
            if ctitle == "" or ccontent_chart == "":
                messages.success(request, "Please complete all information so the seller can respond quickly!")
            else:
                Information.objects.create(ctitle=ctitle, cusername=cusername, cusername1=cusername1,
                                           ccontent_chart=ccontent_chart, cinformation_id=cinformation_id)
                messages.success(request, "Message sent successfully")
        context = {
            'goods': goods,
            'orderinfs': orderinfs,
            'name': content_username,
            'user': user,
            'shoper': shoper,
            'Content': Content,
            'infos': infors,
        }
        return render(request, 'df_user/shoper_information.html', context)
    else:
        if request.method == "POST":
            return render(request, 'df_user/login.html')
    context = {
        'goods': goods,
        'orderinfs': orderinfs,
        'name': content_username,
        'shoper': shoper,
        'Content': Content,
        'infos': infors,
    }
    return render(request, 'df_user/shoper_information.html', context)


def myself_information(request):
    if 'user_id' in request.session:
        uid = request.session['user_id']
        user = UserInfo.objects.get(id=uid)

        goods = GoodsInfo.objects.filter(gunit=user.uname)

        orderinfs = OrderDetailInfo.objects.filter(shopername=user.uname).order_by('-datatime')
        infors = GoodsInfo.objects.filter()

        context = {
            'goods': goods,
            'orderinfs': orderinfs,
            'user': user,
            'infors': infors,
        }
        return render(request, 'df_user/myself_information.html', context)


@user_decorator.login
def message(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    cart_num = CartInfo.objects.filter(user_id=user.id).count()

    persons = Information.objects.filter(cinformation_id=user.id).values('cusername', 'ccheck').distinct().order_by('cusername')

    # checks = Information.objects.filter(cinformation_id=user.id).values('cusername').distinct().order_by('cusername')
    # print("checks:%s,checks.count:%s" % (checks, checks.count()))
    print("Message List: %s, Message Length: %s, Message Count: %s" % (persons, len(persons), persons.count()))

    imgs = UserInfo.objects.filter()
    context = {
        'title': 'Message Center',
        'page_name': 1,
        'user': user,
        'persons': persons,
        'imgs': imgs,
        'guest_cart': 1,
        'cart_num': cart_num,
        'username': user.uname,
        # 'checks':checks,
    }
    return render(request, 'df_user/user_messages.html', context)


@user_decorator.login
def person_message(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    cart_num = CartInfo.objects.filter(user_id=user.id).count()

    persons = Information.objects.filter(cinformation_id=user.id).values('cusername', 'ccheck').distinct().order_by('cusername')

    imgs = UserInfo.objects.filter()

    username = request.GET['username']
    informations = Information.objects.filter()
    logo = UserInfo.objects.get(uname=username)
    print("informations:%s" % (informations))

    # checks = Information.objects.filter(cinformation_id=user.id).values('cusername').distinct().order_by('cusername')
    # print("checks:%s,checks.count:%s" % (checks, checks.count()))

    for information in informations:
        if information.cusername == username:
            information.ccheck = True
            information.save()

    user_name = UserInfo.objects.get(uname=username)

    # persons1 = Information.objects.filter(cusername=cusername).values('cusername1').distinct().order_by('cusername1')
    if request.method == "POST":
        cusername = user.uname
        cusername1 = user_name.uname
        ccontent_chart = request.POST.get('title')
        cinformation_id = user_name.id
        if ccontent_chart == "":
            messages.success(request, "Please enter content!")
        else:
            Information.objects.create(cusername=cusername, cusername1=cusername1,
                                       ccontent_chart=ccontent_chart, cinformation_id=cinformation_id)
            messages.success(request, "Message sent successfully")
            return redirect(reverse("df_user:message"))
    context = {
        'title': 'Message Center',
        'page_name': 1,
        'user': user,
        'informations': informations,
        'persons': persons,
        'imgs': imgs,
        'logo': logo,
        'username': username,
        'user_name': user_name,
        'guest_cart': 1,
        'cart_num': cart_num,
        # 'checks':checks,
        # 'persons1':persons1,
    }
    return render(request, 'df_user/user_messages.html', context)


@user_decorator.login
def tuihuo(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    if request.method == "POST":
        title = request.POST.get('title')
        username = request.POST.get('username')
        username1 = request.POST.get('username1')
        person_number = request.POST.get('person_number')
        order_number = request.POST.get('order_number')
        kuaidi = request.POST.get('kuaidi')
        kuaidi_number = request.POST.get('kuaidi_number')
        address = request.POST.get('address')
        address1 = request.POST.get('address1')
        text = request.POST.get('text')
        if title == "" or username == "" or username1 == "" or person_number == "" or order_number == "" or kuaidi == "" or kuaidi_number == "" or address == "" or address1 == "":
            messages.success(request, "Please complete all required fields!")
        else:
            tuihuoInfo.objects.create(title=title, username=username, username1=username1, person_number=person_number, order_number=order_number, kuaidi=kuaidi, kuaidi_number=kuaidi_number, address=address, address1=address1, text=text)
            messages.success(request, "Submission successful, waiting for approval!")
            return redirect(reverse("df_user:info"))

    context = {
        'title': 'Fill in Return Information',
        'page_name': 1,
        'user': user,
        # 'value':value
    }
    return render(request, 'df_user/tuihuo.html', context)
