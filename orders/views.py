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
        custom_description = request.POST.get('custom_description')
        refrence_image = request.POST.get('refrence_image')

        profile = Profile.objects.get(user=request.user)    

        if product_name :
            try: 
                product = Product.objects.get(name=product_name)
                order = Order.objects.create(
                        customer=profile,
                        product=product,
                        quantity=quantity,
                        deposit=deposit,
                        total_price=product.price * int(quantity),
                        is_customer_order=False
                   ) 
            except Product.DoesNotExist:
                messages.error(request, "Selected product was not found.")
                return redirect('place_order')
        else:
            order = Order.objects.create(
                    customer=profile,
                    quantity=quantity,
                    deposit=deposit,
                    total_price=0, 
                    is_customer_order=True,
                    custom_description=custom_description,
                    refrence_image=refrence_image
                )
        order.save()
        messages.success(request, "Order placed successfully.")
        return redirect('my_orders')
    
    products = Product.objects.all()
    return render(request, 'orders/place_order.html', {'products': products})

def cancel_order(request):
    return render(request, 'orders/cancel_order.html')

def edit_order(request):
    return render(request, 'orders/edit_order.htm')

def my_orders(request):
    
    orders = Order.objects.all()

    return render(request, 'orders/my_orders.html', {'orders': orders})