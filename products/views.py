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
        return redirect('upload_product')
        messages.uccess(request, "Product uploaded successfully!")

    return render(request, 'products/upload_product.html')

def view_products(request):
    return render(request, 'products/view_products.html')


def update_product(request):

    return render(request, 'products/update_product.html')

