from django.urls import path
from . import views

urlpatterns = [
    path('view_products/', views.view_products, name='view_products'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),

]