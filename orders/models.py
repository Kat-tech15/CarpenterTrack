from django.db import models
from decimal import Decimal
from accounts.models import Profile
from products.models import Product

class Order(models.Model):
    customer  = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    total_price= models.DecimalField(max_digits=8, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)    
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('cancelled', 'Cancelled'),
    ], 
    default='Pending')
    is_customer_order = models.BooleanField(default=False)
    custom_description = models.TextField(blank=True, null=True)
    refrence_image = models.ImageField(upload_to='customer_orders/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.product and self.total_price == 0:
            self.total_price =  self.product.price * self.quantity
        
        self.balance =  max(Decimal(str(self.total_price)) - Decimal(str(self.deposit)), Decimal('0.00'))

        if self.deposit <= 0:
            self.status = 'pending'
        elif self.deposit < self.total_price:
            self.status = 'partial'
        else:
            self.status = 'paid'
        
        super().save(*args, **kwargs)
