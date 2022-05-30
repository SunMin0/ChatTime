from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cafe.models import Product
from .forms import AddProductForm
from .cart import Cart



@require_POST
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductForm(request.POST)
    # print('form:',form)
    # print('cart:',cart)
    print('test')
    if form.is_valid():
        cd = form.cleaned_data
        print('폼진입')
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'], size=cd['size'], temp=cd['temp'])
        print('cd:', cd)
        print('product:', product)
        print('is_update:', cd['is_update'])
        print('quantity:', cd['quantity'])
        #size,temp 넣기위해서 추가
    return redirect('cart:detail')









def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:detail')


def detail(request):
    cart = Cart(request)
    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity': product['quantity'], 'is_update': False, 'size': 'L', 'temp': 'H'})
        print("product['quantity_form']:",product['quantity_form'])
    return render(request, 'cart/detail.html', {'cart': cart})