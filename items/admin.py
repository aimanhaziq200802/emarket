from django.contrib import admin
from .models import Category, Item, PurchaseReceipt, ItemStatus

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(PurchaseReceipt)
admin.site.register(ItemStatus)

