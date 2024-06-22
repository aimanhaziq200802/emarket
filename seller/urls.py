from django.urls import path
from . import views

app_name = "seller"

urlpatterns = [
    path('add/', views.add_item, name='add_item'),
    path('my-items/', views.my_items, name='my_items'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('seller-orders/', views.seller_orders, name='seller_orders'), 

]
