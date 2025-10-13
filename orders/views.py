from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Order
from accounts.models import Profile
from products.models import Product 

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity',1))
        deposit = float(request.POST.get('deposit',0))
        custom_description = request.POST.get('custom_description', '')
        refrence_image = request.POST.get('refrence_image')

        profile = Profile.objects.get(user=request.user) 

        if product_id and product_id != "":
            try: 
                product = Product.objects.get(id=product_id)
                total_price = float(product.price) * quantity
                order = Order.objects.create(
                        customer=profile,
                        product=product,
                        quantity=quantity,
                        deposit=deposit,
                        total_price=total_price,
                        is_customer_order=False
                   ) 
            except Product.DoesNotExist:
                messages.error(request, "Selected product was not found.")
                return redirect('place_order', product_id=product_id)
            
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

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    if request.method == "POST":
        order.status = 'Cancelled'
        #order.delete()  # Optional: If you want to delete the order instead of marking it as cancelled
        order.save()
        messages.success(request, "Order cancelled successfully.")
        return redirect('my_orders')
    
    return render(request, 'orders/cancel_order.html', {'order': order})

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    if request.method == "POST":
        new_quantity = int(request.POST.get('quantity', order.quantity))
        new_deposit = float(request.POST.get('deposit', order.deposit))

        order.quantity = new_quantity
        order.deposit = new_deposit
        if order.product:
            order.total_price = order.product.price * new_quantity
        
        order.save()

        messages.success(request, "Order updaed successfully!")
        return redirect('my_orders')


    return render(request, 'orders/edit_order.html', {'order': order})  

@login_required
def my_orders(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(customer=profile).order_by('-created_at') 

    return render(request, 'orders/my_orders.html', {'orders': orders})