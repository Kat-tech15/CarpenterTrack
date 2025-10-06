from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product


def upload_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        Product.objects.create(
            name=name,
            description=description,
            price=price,
        )
        messages.success(request, "Product uploaded successfully!")
        return redirect('upload_product')

    return render(request, 'products/upload_product.html')

def view_products(request):
      
    products = Product.objects.all().order_by('-id')

    return render(request, 'products/view_products.html',{'products':products})


def update_product(request):

    return render(request, 'products/update_product.html')

