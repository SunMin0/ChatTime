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
                # extra = {'product':item['product'],
                #          'price':item['price'],
                #          'quantity':item['quantity'],
                #          'size':item['size'],
                #          'temp':item['temp']
                # }
                #
                # host = get_secret('LOGSTASH_HOST')
                # port = get_secret('LOGSTASH_PORT')
                # logger = logging.getLogger('python-logstash-logger')
                # logger.setLevel(logging.INFO)
                # logger.addHandler(logstash.TCPLogstashHandler(host, port, version=1))
                # logger.addHandler(StreamHandler())
                # logger.info(" 주문내역전송 ",extra=extra)
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})

def order_complete(request):
    print('주문완료')
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    order_item_list = OrderItem.objects.all()
    Current_user = request.user
    c_user = CustomUser.objects.get(username=Current_user)
    for order_item in order_item_list:
        if int(order_id) == int(order_item.order_id):
            print('일치-----')
            print('ID:', c_user.username)
            print('사용자명:', c_user.u_nickname)
            print('성별:', c_user.u_sex)
            print('생년월일:', c_user.birth_year)
            print('주문자명:', order.nick_name)
            print('이메일:', order.email)
            print('총가격:', order.total_price)
            print('주문번호:', order_item.order_id)
            print('주문일:', order.created)
            print('상품명:',order_item.product)
            print('가격:',order_item.price)
            print('수량:',order_item.quantity)
            print('사이즈:',order_item.size)
            print('온도:',order_item.temp)
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