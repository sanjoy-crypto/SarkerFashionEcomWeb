from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.http import JsonResponse


# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')

        context = {'topwears': topwears, 'bottomwears': bottomwears,
                   'mobiles': mobiles, 'laptops': laptops}

        return render(request, 'app/home.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        products = Product.objects.get(id=pk)
        item_in_cart = False
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(
                Q(product=products.id) & Q(user=request.user)).exists()

            context = {'product': products, 'item_in_cart': item_in_cart}
            return render(request, 'app/productdetail.html', context)
        else:
            return redirect('login')


@login_required
def add_to_cart(request):

    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.00
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)

                amount += tempamount

                totalamount = amount+shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})

        else:
            return render(request, 'app/emptycart.html')

    else:
        return redirect('login')


def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.00
        totalamount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }

            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.00
        totalamount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }

            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':

        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0
        shipping_amount = 70.0

        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount

        data = {

            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required
def profile(request):
    if request.method == 'GET':
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-warning'})

    else:
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            division = form.cleaned_data['division']

            reg = Customer(user=user, name=name, phone=phone,
                           locality=locality, city=city, division=division)

            reg.save()

            messages.success(
                request, 'Congratulations!! Register Successfully')

            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-warning'})


@login_required
def address(request):
    customer = Customer.objects.filter(user=request.user)

    return render(request, 'app/address.html', {'customer': customer, 'active': 'btn-warning'})


@login_required
def orders(request):

    op = OrderPlaced.objects.filter(user=request.user)

    return render(request, 'app/orders.html', {'order_placed': op})


@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please enter correct password !!!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/changepassword.html', {
        'form': form
    })

# Mobile


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Samsung' or data == 'Realme' or data == 'Xiaomi':
        mobiles = Product.objects.filter(category='M').filter(brand=data)

    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discount_price__lt=30000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discount_price__gt=30000)

    context = {'mobiles': mobiles}
    return render(request, 'app/mobile.html', context)


# Laptop

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Apple' or data == 'Acer' or data == 'Del' or data == 'HP' or data == 'Lenovo' or data == 'Sony' or data == 'Walton':
        laptops = Product.objects.filter(category='L').filter(brand=data)

    elif data == 'below':
        laptops = Product.objects.filter(
            category='L').filter(discount_price__lt=50000)

    elif data == 'above':
        laptops = Product.objects.filter(
            category='L').filter(discount_price__gt=50000)

    context = {'laptops': laptops}
    return render(request, 'app/laptop.html', context)


# Bottom Wear

def topWear(request, data=None):
    if data == None:
        topWears = Product.objects.filter(category='TW')

    elif data == 'Adidas' or data == 'Park' or data == 'Polo':
        topWears = Product.objects.filter(category='TW').filter(brand=data)

    context = {'topWears': topWears}
    return render(request, 'app/topWear.html', context)


# Bottom Wear


def bottomWear(request, data=None):
    if data == None:
        bottomWears = Product.objects.filter(category='BW')

    elif data == 'Lee' or data == 'Denim':
        bottomWears = Product.objects.filter(category='BW').filter(brand=data)

    context = {'bottomWears': bottomWears}
    return render(request, 'app/bottomWear.html', context)


# Login


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.warning(request, 'Username or Password Incorrect')
    return render(request, 'app/login.html')


def logOut(request):
    logout(request)
    return redirect('login')

# def customerregistration(request):
#     return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()

        context = {'form': form}
        return render(request, 'app/customerregistration.html', context)

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, 'Account was created for ' + str(username))
            return redirect('login')

        context = {'form': form}
        return render(request, 'app/customerregistration.html', context)


@login_required
def checkout(request):

    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount

        totalamount = amount+shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()

    return redirect('orders')
