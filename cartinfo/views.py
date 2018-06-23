from django.shortcuts import render, redirect
from django.http import request, response, HttpResponse
from userinfo.views import login_decorator
from django.db import DatabaseError
from cartinfo.models import CartInfo
import logging
import json
from memberapp.models import Goods
from userinfo.models import UserInfo
# Create your views here.


@login_decorator
def cart_info(request):
    user_id = request.session.get('user_id')
    find_goods = CartInfo.objects.filter(user=user_id)
    cart_foods = {'find_goods': find_goods}
    return render(request, 'cart.html', cart_foods)


@login_decorator
# 添加一个购物车并且跳转
def add_cart(request):
    new_cart = CartInfo()
    user_id = request.session.get('user_id')
    good_id = request.GET.get('goodid')
    good_count = request.GET.get('gcount')
    good_ = Goods.objects.filter(id=good_id)
    user_ = UserInfo.objects.get(id=user_id)
    if len(good_) > 0:
        new_cart.user = user_
        new_cart.good = good_[0]
    else:
        raise '添加购物车失败'
        redirect('/cart/')
    new_cart.ccount = good_count
    try:
        new_cart.save()
    except BaseException as e:
        logging.warning(e)
        raise '数据库插入异常'
        content = {'status': 'Ok', 'text': '添加数据失败'}
        return HttpResponse(json.dumps(content))
    content = {'status': 'Ok', 'text': '添加数据成功'}
    return HttpResponse(json.dumps(content))
