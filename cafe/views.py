from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from cart.forms import AddProductForm
from .forms import ProductForm


@login_required(login_url='/login')
def f_cafe(request):
    return render(request, 'cafe/cafe.html')

@login_required(login_url='/login')
def espresso(request):
    return render(request, 'cafe/espresso.html')

@login_required(login_url='/login')
def bread(request):
    return render(request, 'cafe/bread.html')

@login_required(login_url='/login')
def juice(request):
    return render(request, 'cafe/juice.html')

@login_required(login_url='/login')
def tea(request):
    return render(request, 'cafe/tea.html')


def product_in_tea(request):
    products = Product.objects.filter(available_display=True)
    return render(request, 'cafe/tea.html', {'products': products})

def product_in_espresso(request):
    products = Product.objects.filter(available_display=True)
    return render(request, 'cafe/espresso.html', {'products': products})

def product_in_bread(request):
    products = Product.objects.filter(available_display=True)
    return render(request, 'cafe/bread.html', {'products': products})

def product_in_juice(request):
    products = Product.objects.filter(available_display=True)
    return render(request, 'cafe/juice.html', {'products': products})


def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    return render(request, 'cafe/detail.html', {'product': product, 'add_to_cart': add_to_cart})

@login_required
def create_product(request) :
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/more')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'cafe/create_product.html', context)