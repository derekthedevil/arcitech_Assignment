from django.shortcuts import render,redirect
from .models import ProductTable
from users.models import User_info,Order_history,Payment_history,Cart_table
from users.models import Cart_table
from django.db.models import Q
from django.contrib import messages


# Create your views here.
products = ProductTable.objects.filter(is_available=True)
def home(request):
    data = {}
    if request.user.is_authenticated :
        user_info = User_info.objects.get(uid=request.user.id)
        data['user_info'] = user_info
    global products
    global filtered_products
    products = ProductTable.objects.filter(is_available=True)
    filtered_products = products
    data['products'] = products
    data['cartvalue'] = find_cart_value(request)
    return render(request,'base.html',context=data)

def filter_category(request,str=None):
    data ={}
    if request.user.is_authenticated :
        user_info = User_info.objects.get(uid=request.user.id)
        data['user_info'] = user_info
    q1 = Q(is_available=True)
    q2 = Q(category=str)
    global filtered_products
    filtered_products = products.filter(q1 & q2)
    data['products'] = filtered_products
    data['cartvalue'] = find_cart_value(request)
    return render(request,"base.html",context=data)

def sort_by_price(request,sort_value):
    data ={}
    if request.user.is_authenticated :
        user_info = User_info.objects.get(uid=request.user.id)
        data['user_info'] = user_info
    if sort_value == 'asc' :
        sorted_products = filtered_products.filter(is_available=True).order_by('price')
    else :
        sorted_products = filtered_products.filter(is_available=True).order_by('-price')
    data['products'] = sorted_products
    data['cartvalue'] = find_cart_value(request)
    return render(request,"base.html",context=data)



def find_cart_value(request):
    user_id = request.user.id 
    cart = Cart_table.objects.filter(user_id=user_id)
    return cart.count()

def search_by_price(request):
    data={}
    if request.user.is_authenticated :
        user_info = User_info.objects.get(uid=request.user.id)
        data['user_info'] = user_info
    min=request.POST['min']
    max=request.POST['max']
    q1 = Q(is_available=True)
    q2 = Q(price__gte = min)
    q3 = Q(price__lte = max)
    searched_products= filtered_products.filter(q1 & q2 & q3)
    data['products'] = searched_products
    data['cartvalue'] = find_cart_value(request)
    return render(request,"base.html",context=data)


def add_to_cart(request,product_id):
    if request.user.is_authenticated:
        user = request.user
        product = ProductTable.objects.get(id=product_id)
        q1 = Q(user_id=user.id)
        q2 = Q(product_id=product_id)
        cart_value = Cart_table.objects.filter(q1 & q2)
        if (cart_value.count()>0):
            messages.error(request,"Product is already in the cart ")
        else:
            cart = Cart_table.objects.create(user_id=user,product_id=product,quantity=1)
            cart.save()
            messages.success(request,"Product is added to the cart ")
        return redirect('/')
    else:
        return redirect("/login") 

def show_cart(request):
    data={}
    total_items = 0
    total_price = 0
    cart_count=find_cart_value(request)
    data['cartvalue']=cart_count
    products_in_cart=Cart_table.objects.filter(user_id=request.user.id)
    data['cartproducts']=products_in_cart
    for product in products_in_cart :
        total_items += product.quantity
        total_price += product.product_id.price * product.quantity
    data['total_items'] = total_items
    data['total_price'] = total_price
    return render(request,'home/cart.html',context=data)


def delete(request,cart_id):
    cart = Cart_table.objects.get(id=cart_id)
    cart.delete()
    return redirect("/cart")

def cart_update(request,cart_id,update):
    cart = Cart_table.objects.get(id=cart_id)
    if update == "inc" :
        cart.quantity += 1
        cart.save()
    else :
        if cart.quantity == 1 :
            cart.delete()
        else :
            cart.quantity -= 1 
            cart.save()
    return redirect("/cart")


import razorpay
def cart(request):
    data1={}
    total_items = 0
    total_price = 0
    cart_count=find_cart_value(request)
    data1['cartvalue']=cart_count
    products_in_cart= Cart_table.objects.filter(user_id=request.user.id)
    data1['cartproducts']=products_in_cart
    for product in products_in_cart :
        total_items += product.quantity
        total_price += product.product_id.price * product.quantity
    data1['total_items'] = total_items
    data1['total_price'] = total_price
    if total_price>1 :
        client = razorpay.Client(auth=("rzp_test_97GJ2rvcYmtUV6", "N0lPf0ifPlzeBdQRyueMNDOJ"))
        data = { "amount": int((total_price)*100), "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
    return render(request,'home/cart.html',context=data1)


def order(request,payment_id,amount):
    pay = Payment_history.objects.create(id=payment_id,user_id=request.user,amount=amount)
    cart = Cart_table.objects.filter(user_id=request.user.id )
    user_info = User_info.objects.get(uid=request.user.id)
    for i in cart :
        order = Order_history.objects.create(payment_id=pay,uid=request.user,product_id=i.product_id,address=user_info.address,quantity=i.quantity,price=i.quantity * i.product_id.price)
    cart.delete()
    return redirect("/")