from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Order
from accounts.models import Profile
from products.models import Product 


def place_order(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantinty')
        deposit = request.POST.get('deposit')

        product = Product.objects.get(name=product_name)

        profile = Profile.objects.get(user=request.user)    

        Order.objects.create(
            customer=profile,
            product=product,
            quantity=quantity,
            deposit=deposit
        )
        messages.success(request, "Order placed successfully!")
        return redirect('place_order')
    products = Product.objects.all()
    return render(request, 'orders/place_order.html')

def cancel_order(request):
    return render(request, 'orders/cancel_order.html')

def edit_order(request):
    return render(request, 'orders/edit_order.htm')