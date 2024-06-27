from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from items.models import Item, ItemStatus, PurchaseReceipt
from .models import Cart, CartItem
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.db import models
from django.contrib import messages
from django.contrib.auth import get_user_model


@login_required(login_url="login")
def add_to_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    if item.stock <= 0:
        messages.error(request, "Sorry the item is out of stock.")
        return redirect("items:detail", item_id)

    cart, cart_created = Cart.objects.get_or_create(user=request.user)
    if cart_created:
        cart.save()
    cart_item, item_created = CartItem.objects.get_or_create(user=request.user, item=item, seller=item.seller)

    if item_created:
        cart.cart_items.add(cart_item)
        messages.success(request, "Item added to cart successfully.")
        return redirect("cart:cart")
    else:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Item added to cart successfully.")
        
    cart.save()
    return redirect("cart:cart")
    
@login_required(login_url="login")
def remove_from_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    cart_item = CartItem.objects.get(user=request.user, item=item)
    cart_item.delete()
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.cart_items.all()
    if cart_items:
        newTotal = cart_items.aggregate(models.Sum("total"))["total__sum"]
        newTotal = "{:.2f}".format(newTotal)
        cart.total = newTotal
        cart.save()
        messages.warning(request, "Cart item removed successfully.")
    else:
        cart.delete()
        messages.warning(request, "Cart item removed successfully.")

    return redirect("cart:cart")

@login_required(login_url="login")
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart is None:
        cart_items = []
        summ = 0
    else:
        cart_items = cart.cart_items.all()
        summ = cart_items.aggregate(models.Sum("total"))["total__sum"]
        cart.total = summ
        cart.save()

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "sum": summ,
        },
    )

@login_required(login_url="login")
def purchase(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart is None:
        return redirect("cart:cart")

    out_of_stock = False
    for cart_item in cart.cart_items.all():
        if cart_item.item.stock < cart_item.quantity:
            messages.error(request, f"Sorry, {cart_item.item.title} is out of stock or request quantity exceeds the stock availabililty")
            out_of_stock = True
            break

    if not out_of_stock:
        receipt = PurchaseReceipt.objects.create(buyer=request.user, total=cart.total)
        for cart_item in cart.cart_items.all():
            item = cart_item.item
            item.stock -= cart_item.quantity
            item.sold += cart_item.quantity
            item.save()
            item_status = ItemStatus.objects.create(
                item=item,
                receipt=receipt,
                status='Pending',
                quantity=cart_item.quantity
            )
            receipt.items.add(item)
            cart_item.delete()

        if request.POST.get('delivery_option') == 'delivery':
            User = get_user_model()
            delivery_service_user = User.objects.filter(role='delivery service').first()
            receipt.delivery_service = delivery_service_user

        receipt.save()
        return redirect("user_profile:purchases")

    return redirect("cart:cart")

@require_POST
@login_required(login_url="login")
def update_cart_item_quantity(request):
    data = json.loads(request.body)
    item_id = data["itemId"]
    quantity = data["quantity"]
    cart_item = CartItem.objects.get(user=request.user, item__id=item_id)
    cart_item.quantity = quantity
    cart_item.save()
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.cart_items.all()
    newTotal = cart_items.aggregate(models.Sum("total"))["total__sum"]
    newTotal = "{:.2f}".format(newTotal)
    cart.total = newTotal
    cart.save()
    return JsonResponse({'newTotal': newTotal})


@login_required(login_url="login")
def update_cart_item_status(request, item_status_id):
    item_status = get_object_or_404(ItemStatus, id=item_status_id)
    if request.user != item_status.item.seller:
        messages.error(request, 'You do not have permission to update this item status.')
        return redirect('user_profile:seller_orders')

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        if new_status in dict(ItemStatus.STATUS_CHOICES):
            item_status.status = new_status
            item_status.save()
            messages.success(request, 'Item status updated successfully.')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('seller:seller_orders')

@login_required(login_url="login")
def update_delivery_status(request, item_status_id):
    item_status = get_object_or_404(ItemStatus, id=item_status_id)
    if request.user.role != 'delivery service':
        messages.error(request, 'You do not have permission to update this item delivery status.')
        return redirect('items:index')

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        if new_status in dict(ItemStatus.STATUS_CHOICES):
            item_status.status = new_status
            if new_status == 'Delivered':
                item_status.receipt.update_status()
            item_status.save()
            messages.success(request, 'Delivery status updated successfully.')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('delivery:delivery_dashboard')