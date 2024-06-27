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

    delivery_items = ItemStatus.objects.filter(receipt__delivery_service=request.user, status__in=['Ready for Delivery', 'Out for Delivery']).order_by('created_at')
    order_history = ItemStatus.objects.filter(receipt__delivery_service=request.user, status__in=['Delivered', 'Completed']).order_by('-created_at')

    return render(request, 'delivery/delivery_dashboard.html', {'delivery_items': delivery_items, 'order_history': order_history})

