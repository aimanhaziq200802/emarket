from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import *
from django.contrib import messages
from django.shortcuts import redirect

#Delivery dashboard view
@login_required(login_url="login")
def delivery_dashboard(request):
    if request.user.role != 'delivery service':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('items:index')

    delivery_items = ItemStatus.objects.filter(status='Out for Delivery', receipt__delivery_service=request.user)
    if not delivery_items:
        messages.info(request, 'No items found for delivery.')
    return render(request, 'delivery/delivery_dashboard.html', {'delivery_items': delivery_items})