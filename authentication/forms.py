from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Location

class RegisterUserForm(UserCreationForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label="Select your location",
        required=False,
        label='Location',
        widget=forms.Select(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}),
    )

    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('delivery service', 'Delivery Service'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Role',
        widget=forms.Select(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}),
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}),
        strip=False,
    )

    address = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'location', 'role', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}),
        }
