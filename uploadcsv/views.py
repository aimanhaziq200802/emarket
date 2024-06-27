import csv
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from items.models import Item, Category 
from authentication.models import CustomUser 

def upload_csv(request):
    if not request.user.is_staff:
        return redirect("items:index")
    
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                category, created = Category.objects.get_or_create(name=row['category'])
                seller = CustomUser.objects.get(username=row['seller'])
                
                item = Item(
                    title=row['title'],
                    description=row['description'],
                    price=row['price'],
                    stock=row['stock'],
                    category=category,
                    seller=seller
                )

                image_url = row['image']
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_name = image_url.split("/")[-1]
                    item.image.save(image_name, ContentFile(image_response.content), save=False)

                item.save()

            messages.success(request, 'Items uploaded successfully.')
            return redirect('items:index')
    else:
        form = CSVUploadForm()

    return render(request, 'uploadcsv/upload_csv.html', {'form': form})
