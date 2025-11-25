from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .models import Product


def upload_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            image=image
        )
        messages.success(request, "Product uploaded successfully!")
        return redirect('view_products')

    return render(request, 'products/upload_product.html')

def view_products(request):
      
    products = Product.objects.all().order_by('-id')

    return render(request, 'products/view_products.html',{'products':products})

def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def update_product(request, pk): 
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')

        if request.FILES.get('image'):
            product.image = request.FILES['image']
        
        product.save()
        return redirect('view_products')
    
    return render(request, 'products/update_product.html', {'product': product})

@login_required(login_url='login_view')
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully.")
        return redirect('view_products')
    
    return render(request, 'products/delete_product.html', {'produt': product})

