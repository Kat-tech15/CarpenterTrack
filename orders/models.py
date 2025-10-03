from django.db import models
from accounts.models import Profile
from products.models import Product

class Order(models.Model):
    customer  = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    deposit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.customer.user.username} - {self.product.name} - {self.quantity} - {self.deposit}"
