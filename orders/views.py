from django.shortcuts import render,redirect
from django.contrib import messages
from . models import Order


def place_order(request):
    if request.method == "POST":
        order_user = request.POST.get('order_user')
        order_phone_number = request.POST.get('order_phone_number')
        order_email = request.POST.get('order_email')
        order_location = request.POST.get('order_location')
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantinty')
        deposit = request.POST.get('deposit')

        Order.objects.create(
            order_user=order_user,
            order_phone_number=order_phone_number,
            order_email=order_email,
            order_location=order_location,
            product_name=product_name,
            quantity=quantity,
            deposit=deposit
        )
        return redirect('place_order')
        messages.success(request, "Order placed successfully!")
    return render(request, 'orders/place_order.html')

def cancel_order(request):
    return render(request, 'orders/cancel_order.html')

def edit_order(request):
    return render(request, 'orders/edit_order.htm')