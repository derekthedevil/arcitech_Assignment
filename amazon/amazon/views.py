from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from products.models import ProductTable
from users.models import User_info,Payment_history,Order_history

def user_login(request):
    data ={}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/")
    if request.method=="POST":
        uname=request.POST['username']
        upass=request.POST['password']
        if (uname=="" or upass==""):
            data['error_msg']="Fields cant be empty"
        elif(not User.objects.filter(username=uname).exists()):
            data['error_msg']=uname + " user does not exist"
        else:
            user=authenticate(username=uname,password=upass)
            if user is None:
                data['error_msg']="Wrong password"
            else:
                login(request,user)
                if user.is_superuser:
                    return redirect("/admin")
                else:
                    return redirect("/")
    return render(request,'user/login.html',context=data)


def user_register(request):
    data ={}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/")
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if (username=="" or password=="" or password2==""):
            data['error_msg']="Fields cant be empty"
        elif(password!=password2):
            data['error_msg']="Password Does not matched"
        elif(User.objects.filter(username=username).exists()):
            data['error_msg']=username + " already exist"
        else:
            user=User.objects.create(username=username)
            User_info.objects.create(uid=user)
            user.set_password(password)
            user.save()
            return redirect("/")
    return render(request,'user/register.html',context=data)


def user_logout(request):
    logout(request)
    return redirect('/')


def admin_panel(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect("/")
    return render(request,'admin/admin.html')


def add_product(request):
    data ={}
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description=request.POST.get('description')
        quantity=request.POST.get('quantity')
        category=request.POST.get('category')
        image = request.FILES['image']
        is_available=(request.POST.get('is_available',False)) and ('is_available' in request.POST)
        product=ProductTable.objects.create(name=name,price=price,description=description,quantity=quantity,category=category,images=image,is_available=is_available)
        product.save()      
        return redirect("/admin/product/view/",context=data)
    return render(request,'admin/product/add_product.html')


def view_products(request):
    data ={}
    all_product = ProductTable.objects.all()
    data['products'] = all_product
    return render(request,'admin/product/view_product.html',context=data)


def delete(request,int):
    product = ProductTable.objects.get(id=int)
    product.is_available = 0
    product.save()
    return redirect('/admin/product/view')


def edit_product(request,int):
    data = {}
    product = ProductTable.objects.get(id=int)
    data['product'] = product
    if request.method=='POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description=request.POST.get('description')
        product.quantity=request.POST.get('quantity')
        product.category=request.POST.get('category')
        if 'image' in request.FILES:
            product.images = request.FILES['image']
        product.save()
        return redirect('/admin/product/view')
    return render(request, 'admin/product/edit_product.html',context=data)


def generel_settings(request):
    user_id = request.user.id 
    user = User.objects.get(id=user_id)
    data={}
    user_info = User_info.objects.get(uid=user_id)
    data['user_info'] = user_info
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST['email']
        phone = request.POST['phone']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        pincode = request.POST['pincode']
        address = request.POST['address']
        user.username = username
        user.email = email
        user.last_name = lastname
        user.first_name = firstname
        user.save()
        user_info = User_info.objects.get(uid=user_id)
        user_info.phone = phone
        user_info.pincode = pincode
        user_info.address = address
        if 'image' in request.FILES :
            user_info.image = request.FILES['image']
        user_info.save()
        data['user_info'] = user_info
    return render(request,"users/general_settings.html",context=data)



def order_history(request):
    list1 = []
    data ={}
    payments = Payment_history.objects.filter(user_id=request.user.id)
    if payments != None :
        for i in payments :
            orders = Order_history.objects.filter(payment_id=i.id)
            list1.append(orders)
        data["orders"] = list1
    else :
        pass
    return render(request,"users/order_history.html",context=data)