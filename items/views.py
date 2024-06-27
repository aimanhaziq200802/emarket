from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AddItemForm
from .models import Category, Item
from django.contrib.auth.decorators import login_required

# Index view
def index(request):
    all_messages = messages.get_messages(request)

    if request.user.is_authenticated:
        if request.user.role == 'delivery service':
            return redirect('delivery:delivery_dashboard')
        
        elif request.user.is_staff:
            return redirect('adminapp:admin_dashboard')
        
        elif request.user.role == 'seller':
            return redirect('seller:seller_orders')

        elif request.user.role == 'seller':
            items = Item.objects.filter(is_sold=False)
    
        else:
            user_location = request.user.location
            items = Item.objects.filter(
                seller__covered_locations__name=user_location,
                is_sold=False
            )[:8]

        for item in items:
            if item.is_on_sale:
                item.discount = item.discounted_price()
    else:
        items = Item.objects.filter(is_sold=False)[:8]

        for item in items:
            if item.is_on_sale:
                item.discount = item.discounted_price()

    return render(
        request,
        "items/index.html",
        {
            "items": items,
            "all_messages": all_messages,
        }
    )

# Detail view
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.is_on_sale:
        item.discount = item.discounted_price()
    return render(
        request,
        "items/detail.html",
        {
            "item": item,
        },
    )

# Browse view
def browse(request):
    items = [] 
    query = ""
    category_id = 0
    categories = Category.objects.all()
    
    if request.user.is_authenticated:
        if request.user.role == 'delivery service':
            messages.error(request, 'You do not have access to browse items.')
            return redirect('delivery:delivery_dashboard')
        
        elif request.user.is_staff:
            messages.error(request, 'You do not have access to browse items.')
            return redirect('adminapp:admin_dashboard')
    
    query = request.GET.get("query", "")
    category_id = request.GET.get("category", 0)
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(seller__username__icontains=query)
        )

    return render(
        request,
        "items/browse.html",
        {
            "items": items,
            "query": query,
            "categories": categories,
            "category_id": int(category_id),
        },
    )

# Popular items view
def popular_items(request):
    if request.user.is_authenticated:
        if request.user.role == 'delivery service':
            messages.error(request, 'You do not have access to browse items.')
            return redirect('delivery:delivery_dashboard')
        
        elif request.user.is_staff:
            messages.error(request, 'You do not have access to browse items.')
            return redirect('adminapp:admin_dashboard')
        
    popular_items = Item.objects.filter(is_sold=False).order_by('-sold')[:8]
    
    for item in popular_items:
        if item.is_on_sale:
            item.discount = item.discounted_price()

    context = {
        'popular_items': popular_items,
    }
    return render(request, 'items/popular_items.html', context)

# New arrivals view
def new_arrivals(request):
    if request.user.is_authenticated:
        if request.user.role == 'delivery service':
            messages.error(request, 'You do not have access to browse items.')
            return redirect('delivery:delivery_dashboard')
        
        elif request.user.is_staff:
            messages.error(request, 'You do not have access to browse items.')
            return redirect('adminapp:admin_dashboard')
        
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[:20]
    return render(request, 'items/new_arrivals.html', {'items': items})

#About view
def about(request):
    return render(request, 'items/about.html')