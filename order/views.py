from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from users.models import CustomUser
from .models import *
from cart.cart import Cart
from .forms import *
from django.views.generic.base import View
from django.http import JsonResponse



def order_list(request):
    #오브젝트 불러오기
    order_list = OrderItem.objects.all()
    total_price = 0
    for order in order_list:
        total_price += order.price
    return render(request, 'order/orderitem_list.html', {'order_list':order_list, 'total_price' : total_price})





def customer_order_list(request):
    #오브젝트 불러오기
    u_id = CustomUser.objects.filter(is_manager=0,is_master=0)
    o_id = Order.objects.filter()

    print(u_id)
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
                print('item:',item)
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         size=item['size'],
                                         temp=item['temp']
                                         )
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})


def order_complete(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    return render(request, 'order/complete.html', {'order': order})


class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        cart = Cart(request)
        total_price = cart.get_total_price()
        print('total_price:',total_price)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total_price
            order.save()
            for item in cart:
                print(item)
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


# @staff_member_required
# def admin_order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'order/admin/detail.html', {'order': order})
#
#
# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('order/admin/pdf.html', {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
# #    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0]+'/css/pdf.css')])
#     return response


