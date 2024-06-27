from django import forms
from .models import Item
from authentication.models import Location
from items.models import Category

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    covered_locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Covered Locations'
    )

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'image', 'category', 'is_on_sale', 'discount', 'stock', 'sold']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class AddLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

