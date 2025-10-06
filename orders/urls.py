from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('edit_order/', views.edit_order, name='edit_order'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
]