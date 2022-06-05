from django.shortcuts import render
from config.settings import get_secret
from users.models import CustomUser
from .models import *
from cart.cart import Cart
from .forms import *
from django.views.generic.base import View
from django.http import JsonResponse
import logging
from logging import StreamHandler
import logstash
import datetime

# 로그스태시
host = get_secret('LOGSTASH_HOST')
port = get_secret('LOGSTASH_PORT')
logger = logging.getLogger('python-logstash-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logstash.TCPLogstashHandler(host, port, version=1))
logger.addHandler(StreamHandler())


def order_list(request):
    #오브젝트 불러오기
    order_list = OrderItem.objects.all()
    total_price = 0
    for order in order_list:
        total_price += order.price
    return render(request, 'order/orderitem_list.html', {'order_list':order_list, 'total_price' : total_price})

def customer_order_list(request):
    #오브젝트 불러오기
    order_list = OrderItem.objects.all()
    return render(request, 'order/common_orderitem_list.html', {'order_list':order_list})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         size=item['size'],
                                         temp=item['temp'],
                                         )
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})

def order_complete(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    order_item_list = OrderItem.objects.all()
    Current_user = request.user
    c_user = CustomUser.objects.get(username=Current_user)

    for order_item in order_item_list:
        if int(order_id) == int(order_item.order_id):
            # UTC 타임을 한국에 맞게 수정
            order_date = str(datetime.datetime.now())
            order_date = order_date.replace(' ', 'T')
            order_date = order_date + "+09:00"

            extra = {'order_date':order_date,
                     'order_number':int(order_item.order_id),
                     'uid': c_user.username,
                     'sex':c_user.u_sex,
                     'birth':int(c_user.birth_year),
                     'email':order.email,
                     'total_price':int(order.total_price),
                     'product_name':order_item.product.name,
                     'product_price':int(order_item.price),
                     'quantity':int(order_item.quantity),
                     'size':order_item.size,
                     'temp':order_item.temp
                     }
            # 로그스태시 전송
            logger.info(" 주문내역전송 ", extra=extra)
    return render(request, 'order/complete.html', {'order': order})

class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)
        cart = Cart(request)
        total_price = cart.get_total_price()
        Current_user = request.user
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total_price
            order.user = Current_user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         size=item['size'],
                                         temp=item['temp']
                                         )
            cart.clear()
            data = {
                "order_id": order.id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()
            order.paid = True
            order.save()

            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)