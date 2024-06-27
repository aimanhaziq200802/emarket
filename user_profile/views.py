from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from items.models import Item
from items.models import PurchaseReceipt
from .forms import ItemForm
from authentication.forms import RegisterUserForm 
from .forms import EditProfileForm
from django.contrib import messages
from items.models import ItemStatus

@login_required(login_url="login")
def user_profile(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile:user_profile')
    else:
        form = RegisterUserForm(instance=request.user)

    return render(request, 'user_profile/profile.html', {'form': form})

@login_required(login_url="login")
def purchase_history(request):
    receipts = PurchaseReceipt.objects.filter(buyer=request.user).order_by('-date')
    return render(
        request,
        "user_profile/purchase_history.html",
        {
            "receipts": receipts,
        },
    )

@login_required(login_url="login")
def update_item_status(request, item_status_id):
    item_status = get_object_or_404(ItemStatus, id=item_status_id)
    if request.user != item_status.item.seller and not request.user.is_staff:
        messages.error(request, 'You do not have permission to update this item status.')
        return redirect('user_profile:purchases')

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        if new_status in dict(ItemStatus.STATUS_CHOICES):
            item_status.status = new_status
            item_status.seller_confirmed = True
            item_status.save()
            item_status.receipt.update_status()
            messages.success(request, 'Item status updated successfully.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('user_profile:purchases')

@login_required(login_url="login")
def my_items(request):
    seller_items = Item.objects.filter(seller=request.user)
    return render(request, 'user_profile/my_items.html', {'seller_items': seller_items})

@login_required(login_url="login")
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.user != item.seller:
        return redirect('user_profile:my_items')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('user_profile:my_items')
    else:
        form = ItemForm(instance=item)

    return render(request, 'user_profile/edit_item.html', {'form': form, 'item': item})

@login_required(login_url="login")
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile:user_profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'user_profile/edit_profile.html', {'form': form})

@login_required(login_url="login")
def seller_orders(request):
    if request.user.role != 'seller':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('items:index')

    seller_items = ItemStatus.objects.filter(item__seller=request.user, status='Pending').order_by('created_at')
    if not seller_items:
        messages.info(request, 'No pending items found for this seller.')
    return render(request, 'user_profile/seller_orders.html', {'seller_items': seller_items})

