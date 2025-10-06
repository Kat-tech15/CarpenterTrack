from django.db import models
from accounts.models import Profile
from products.models import Product

class Order(models.Model):
    customer  = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_price= models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)    

    is_customer_order = models.BooleanField(default=False)
    custom_description = models.TextField(blank=True, null=True)
    refrence_image = models.ImageField(upload_to='customer_orders/', blank=True, null=True)

    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ], 
    default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *rgs, **kwargs):
        if self.total_price and self.deposit is not None:
            self.balance = self.total_price - self.deposit
        super().save(*rgs, **kwargs)

    def __str__(self):
        if self.is_customer_order:
            return f"Custom Order by {self.customer.user.username}"
        return f"{self.customer.user.username} - {self.product.name if self.product else 'Custom'} - {self.quantity}"

#class payment(models.Model):
