from django import forms
from items.models import Item
from authentication.models import CustomUser

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'discount', 'image', 'category', 'stock', 'is_on_sale', 'is_sold']
        
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['description'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['price'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['discount'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['image'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['category'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['stock'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['is_on_sale'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_sold'].widget.attrs.update({'class': 'form-check-input'})

        self.fields['image'].label = "Change Image"

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'location', 'covered_locations', 'role', 'address']
        
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['location'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['covered_locations'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['covered_locations'].widget.attrs['multiple'] = 'multiple' 
        self.fields['role'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['address'].widget.attrs.update({'class': 'form-control form-control-lg'})

        self.fields['location'].label = "Select a Location (for Optimized Results)"
