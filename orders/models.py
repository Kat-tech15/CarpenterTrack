from django.db import models
from django.conf import settings
from accounts.models import Profile
from products.models import Product

class Order(models.Model):
    order_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_phone_number = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_email = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_location = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    deposit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.product_name} - {self.quantity} - {self.deposit}"
