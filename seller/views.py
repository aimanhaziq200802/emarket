from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from items.models import *
from items.forms import *
from user_profile.forms import *

# Add item view
@login_required(login_url="login")
def add_item(request):
    if not request.user.role == 'seller':
        return redirect("items:index")

    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            messages.success(request, "Item added successfully.")
            return redirect("seller:my_items")
        else:
            print(form.errors) 
    else:
        form = AddItemForm()

    return render(
        request,
        "seller/add_item.html",
        {"form": form},
    )

@login_required(login_url="login")
def my_items(request):
    seller_items = Item.objects.filter(seller=request.user)
    return render(request, 'seller/my_items.html', {'seller_items': seller_items})

@login_required(login_url="login")
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # Check if the user has permission to edit this item
    if request.user != item.seller:
        # You might want to customize this behavior (e.g., show a message, redirect to an error page)
        return redirect('seller:my_items')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item edited successfully.")
            return redirect('seller:my_items')
    else:
        form = ItemForm(instance=item)

    return render(request, 'seller/edit_item.html', {'form': form, 'item': item})

@login_required(login_url="login")
def seller_orders(request):
    if request.user.role != 'seller':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('items:index')

    # Fetch only pending items for the seller
    seller_items = ItemStatus.objects.filter(item__seller=request.user, status='Pending').order_by('created_at')
    if not seller_items:
        messages.info(request, 'No pending items found for this seller.')
    return render(request, 'seller/seller_orders.html', {'seller_items': seller_items})