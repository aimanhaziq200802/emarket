from django.db import models
from items.models import Item
from authentication.models import CustomUser

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="seller", null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ready for Pickup', 'Ready for Pickup'),
        ('Confirmed', 'Confirmed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    delivery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.item.title} - {self.quantity} - {self.total}"

    def save(self, *args, **kwargs):
        self.total = self.item.discounted_price() * self.quantity 
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem, blank=True, related_name="cart_items")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)

    def __str__(self):
        return f"{self.user} - {self.total}"
    
    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)