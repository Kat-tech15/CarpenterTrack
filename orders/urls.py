from django.urls import path
from . import views

urlpatterns = [
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),
    path('edit_order/', views.edit_order, name='edit_order'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('update/order/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
]