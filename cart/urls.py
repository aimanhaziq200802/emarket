from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add-item/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove-item/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("purchase/", views.purchase, name="purchase"),
    path("update-cart-item-quantity/", views.update_cart_item_quantity, name="update_cart_item_quantity"),
    path('update_cart_item_status/<int:item_status_id>/', views.update_cart_item_status, name='update_cart_item_status'),
    path('update_delivery_status/<int:item_status_id>/', views.update_delivery_status, name='update_delivery_status'),

]
