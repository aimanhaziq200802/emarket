from django.conf import settings
from django.db import models
from decimal import Decimal
from authentication.models import CustomUser
from datetime import timedelta
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="items_listed")
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return f"{self.title} | {self.category} | ${self.price}"

    def discounted_price(self):
        return self.price - self.price * self.discount / 100
    
    def time_ago(self):
        now = timezone.now()
        diff = now - self.created_at
        
        if diff < timedelta(minutes=1):
            return "just now"
        elif diff < timedelta(hours=1):
            minutes = int(diff.seconds / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff < timedelta(days=1):
            hours = int(diff.seconds / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days} day{'s' if days > 1 else ''} ago"
        else:
            return self.created_at.strftime("%Y-%m-%d %H:%M")

class ItemStatus(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ready for Pickup', 'Ready for Pickup'),
        ('Ready for Delivery', 'Ready for Delivery'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Completed', 'Completed'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_statuses")
    receipt = models.ForeignKey('PurchaseReceipt', on_delete=models.CASCADE, related_name="item_statuses")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now) 

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = self.item.created_at
        super().save(*args, **kwargs)
        self.receipt.update_status()
        
class PurchaseReceipt(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through=ItemStatus, related_name="purchase_receipts")
    total = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    delivery_service = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries', default=None)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Order Received', 'Order Received'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    status_updated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buyer.username} | {self.total} | {self.date}"

    def update_status(self):
        if all(item_status.status in ['Completed', 'Delivered'] for item_status in self.item_statuses.all()):
            self.status = 'Order Received'
            self.status_updated = True
            self.save()