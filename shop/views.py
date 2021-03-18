from django.shortcuts import render,redirect
from .models import Product, OrderHead, UserCart, OrderDetail,Counter, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models import Sum, F, FloatField
from django.db import transaction
from sequences import Sequence
from django.contrib.auth import settings
order_num = Sequence("order_num")


# Create your views here.

""" def index(request):
    products_list = Product.objects.all().order_by('id')
    item_name = request.GET.get('item_name')
    if item_name!='' and item_name is not None:
        products_list = products_list.filter(name__icontains=item_name)
    paginator = Paginator(products_list,8)
    page = request.GET.get('page')
    products_list = paginator.get_page(page) 
    context = {
        'product_list':products_list,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            print('authenticated')
            item_id = Product.objects.get(id=request.POST["item_id"])
            user = request.user
            add_to_cart(item_id,user)
            return redirect('shop:index')
        else :
            print('not logged')
            return redirect(settings.LOGIN_URL)
    return render(request,'shop/index.html',context) """

def categories(request):
    category_list = Category.objects.all()
    context = {
        'categories':category_list,
    }
    return render(request,'shop/category.html',context)

def itemByCategory(request,category):
    products_list = Product.objects.filter(category=category)
    paginator = Paginator(products_list,8)
    page = request.GET.get('page')
    products_list = paginator.get_page(page) 
    context = {
        'product_list':products_list,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            print('authenticated')
            item_id = Product.objects.get(id=request.POST["item_id"])
            user = request.user
            print('request path',request.path)
            add_to_cart(item_id,user)
            return redirect(request.path)
        else :
            print('not logged')
            return redirect(settings.LOGIN_URL)
    return render(request,'shop/index.html',context)

def add_to_cart(item_id,user):
    user_cart_exists = UserCart.objects.filter(user=user,item=item_id).values('quantity')
    if user_cart_exists :
        qty = user_cart_exists[0]['quantity']
        quantity = qty+1
        UserCart.objects.filter(user=user,item=item_id).update(quantity=quantity)
    else:
        quantity =1
        usercart = UserCart(item=item_id,user=user,quantity=quantity)
        usercart.save()
    return

def detail(request,id):
    product = Product.objects.get(id=id)
    if request.method=="POST":
        item_id = Product.objects.get(id=request.POST["item_id"])
        user = request.user
        add_to_cart(item_id,user)
        return HttpResponseRedirect(request.path_info)
    context = {
        'product':product,
    }
    return render(request,'shop/detail.html',context)

@login_required
@transaction.atomic
def checkout(request):
    total = request.session['total']
    context = {
        'total':total,
    }
    if request.method =="POST":
        name = request.POST.get('name',"")
        email = request.POST.get('email',"")
        address = request.POST.get('address',"")
        city = request.POST.get('city',"")
        state = request.POST.get('state',"")
        zip = request.POST.get('zip',"")
        items = UserCart.objects.filter(user=request.user).values_list('item','quantity')
        save_pt = transaction.savepoint()
        order_id = order_num.get_next_value()
        order = OrderHead(order_id=order_id,name=name,email=email,address=address,city=city,state=state,zipcode=zip,amount=total['total_amount'])
        order.save()
        try:
            for (item,qty) in items:
                order_detail = OrderDetail(order_id=order_id,items=Product.objects.get(id=item),quantity=qty)
                order_detail.save()
        except :
            transaction.savepoint_rollback(save_pt)
        else:
            UserCart.objects.filter(user=request.user).delete()
            return redirect('shop:index')
    return render(request,'shop/checkout.html',context)

@login_required
def userCart(request):
    user = request.user
    cart_items = UserCart.objects.filter(user=user)
    context = {}
    if cart_items:
        total_amount = UserCart.objects.filter(user=user).aggregate(total_amount=Sum(F('item__disc_price')*F('quantity'),output_field=FloatField()),total_quantity=Sum('quantity'))
        #cart_total = Product.objects.filter(id__in=item_values)
        context={
            'cart_item':cart_items,
            'total_amount':total_amount,
            }
        request.session['total'] = total_amount
    if 'remove' in request.POST:
        id = request.POST.get("remove_id")
        UserCart.objects.filter(id=id).delete()
        return redirect("shop:cart")
    if 'decrease' in request.POST:
        id = request.POST.get("remove_id")
        usercart = UserCart.objects.get(id=id)
        print('before',usercart.quantity)
        usercart.quantity = usercart.quantity-1
        if usercart.quantity == 0:
            print('inside zero')
            UserCart.objects.filter(id=id).delete()
        else:
            print('after',usercart.quantity)
            usercart.save()
        return redirect("shop:cart")
    if 'increase' in request.POST:
        id = request.POST.get("remove_id")
        usercart = UserCart.objects.get(id=id)
        print('before',usercart.quantity)
        usercart.quantity = usercart.quantity+1
        usercart.save()
        return redirect("shop:cart")    
    return render(request,'shop/cart.html',context)