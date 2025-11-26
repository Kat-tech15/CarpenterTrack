from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from . models import Order
from accounts.models import Profile
from products.models import Product 

@login_required(login_url='login_view')
def place_order(request, product_id=None):

    
    profile = Profile.objects.get(user=request.user) 
    products = Product.objects.all()

    if request.method == "POST":
        order_type = request.POST.get('order_type', 'product')
        quantity = int(request.POST.get('quantity',1))
        deposit = float(request.POST.get('deposit',0))
        custom_description = request.POST.get('custom_description', '')
        refrence_image = request.POST.get('refrence_image')


        if order_type == 'product':
            posted_product_id =  request.POST.get('product_id')
            if posted_product_id:
                try:
                    product = Product.objects.get(id=posted_product_id)        
                    order = Order.objects.create(
                            customer=profile,
                            product=product,
                            quantity=quantity,
                            deposit=deposit,
                            is_customer_order=False,
                    )
                    messages.success(request, "Product order placed successfully.")
                    return redirect('my_orders')
                except Product.DoesNotExist:
                    messages.error(request, "Selected product was not found.")
                    return redirect('place_order')
            else:
                messages.error(request, "No product selected.")
            
        elif order_type == 'custom':
            unit_price =  float(request.POST.get('unit_price', 0))
            total_price = unit_price * quantity

            Order.objects.create(
                customer=profile,
                product=None,
                quantity=quantity,
                deposit=deposit,
                total_price=total_price,
                is_customer_order=True,
                custom_description=custom_description,
                refrence_image=refrence_image
            )
            messages.success(request, "Custom order placed successfully.")
            return redirect('my_orders')
    
    return render(request, 'orders/place_order.html', {'products': products})


@login_required(login_url='login_view')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    if request.method == "POST":
        if order.status in ['pending', 'partial']:
            order.status = 'cancelled'
            order.save()
            messages.success(request, "Order cancelled successfully.")
        else:
            messages.error(request, "You cannot cancel an order that is fully paid.")
        return redirect('my_orders')
    
    return render(request, 'orders/cancel_order.html', {'order': order})

@login_required(login_url='login_view')
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    if request.method == "POST":
        new_quantity = int(request.POST.get('quantity', order.quantity))
        new_deposit = float(request.POST.get('deposit', order.deposit))
        new_description = request.POST.get('custom_desription', order.custom_description)
        new_image =  request.POST.get('reference_image')

        order.quantity = new_quantity
        order.deposit = new_deposit
        order.custom_description = new_description
        
        if new_image:
            order.refrence_image = new_image

        if order.is_customer_order:
            unit_price =  float(request.POST.get('unit_price', 0))
            order.total_price = unit_price * new_quantity
        
        else:
            order.total_price = float(order.product.price) * new_quantity
        
        order.save()

        messages.success(request, "Order updaed successfully!")
        return redirect('my_orders')
    
    unit_price = 0
    if order.is_customer_order and order.quantity:
        unit_price = float(order.total_price) / order.quantity

    return render(request, 'orders/edit_order.html', {'order': order, 'unit_price': unit_price})  

@login_required(login_url='login_view')
def my_orders(request):

    profile = Profile.objects.get(user=request.user)
    active_orders = Order.objects.filter(customer=profile).exclude(status='cancelled') 
    cancelled_orders = Order.objects.filter(customer=profile, status='cancelled')

    return render(request, 'orders/my_orders.html', {'active_orders': active_orders, 'cancelled_orders': cancelled_orders})

#@user_passes_test(lambda u: u.is_superuser)
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    messages.success(request, f"Order #{order.id} status updated to '{status}'.")
    return redirect('admin_orders')


#@user_passes_test(lambda u: u.is_superuser)
def admin_orders(request):
    all_orders = Order.objects.all().order_by('-id')

    return render(request, 'orders/all_orders.html', {'all_orders':all_orders})

