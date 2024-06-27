from django.shortcuts import render
from items.models import *
from authentication.models import *
from items.forms import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
#Admin dashboard view
@login_required(login_url="login")
def admin_dashboard(request):
    categories = Category.objects.all()
    locations = Location.objects.all()
    return render(request, 'adminapp/admin_dashboard.html', {
        'categories': categories,
        'locations': locations,
    })

# Add category view
@login_required(login_url="login")
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('adminapp:admin_dashboard') 
    else:
        form = AddCategoryForm()
    
    return render(request, 'adminapp/add_category.html', {'form': form})

# Edit category view
@login_required(login_url="login")
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.info(request, 'Category changed successfully.')
            return redirect('adminapp:admin_dashboard')
    else:
        form = AddCategoryForm(instance=category)
    
    return render(request, 'adminapp/edit_category.html', {'form': form, 'category': category})

# Delete category view
@login_required(login_url="login")
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.error(request, 'Category deleted successfully.')
    return redirect('adminapp:admin_dashboard')

# Add location view
@login_required(login_url="login")
def add_location(request):
    if request.method == 'POST':
        form = AddLocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location added successfully.')
            return redirect('adminapp:admin_dashboard') 
    else:
        form = AddLocationForm()
    
    return render(request, 'adminapp/add_location.html', {'form': form})

# Edit location view
@login_required(login_url="login")
def edit_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    
    if request.method == 'POST':
        form = AddLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.info(request, 'Location changed successfully.')
            return redirect('adminapp:admin_dashboard')
    else:
        form = AddLocationForm(instance=location)
    
    return render(request, 'adminapp/edit_location.html', {'form': form, 'location': location})

# Delete location view
@login_required(login_url="login")
def delete_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    location.delete()
    messages.error(request, 'Location deleted successfully.')
    return redirect('adminapp:admin_dashboard')