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
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'], size=cd['size'], temp=cd['temp'])
    return redirect('cart:detail')

def add2(request, data):
    product_id = data['product_id']
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=data['quantity'], is_update=False, size=data['size'], temp=data['temp'])
    return product.name

def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')


def detail(request):
    cart = Cart(request)
    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity': product['quantity'], 'is_update': False, 'size': 'L', 'temp': 'H'})
    return render(request, 'cart/detail.html', {'cart': cart})