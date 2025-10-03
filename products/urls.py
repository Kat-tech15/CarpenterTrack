from django.urls import path
from . import views

urlpatterns = [
    path('view_products/', views.view_products, name='view_products'),
    path('update_products/', views.update_product, name='update_product'),
    path('upload_product/', views.upload_product, name='upload_product'),
]