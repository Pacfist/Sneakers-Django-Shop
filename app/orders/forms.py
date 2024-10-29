import re
from django import forms
from .models import Order, OrderItem

class CreateOrderForm(forms.ModelForm):
    full_name = forms.CharField(label="Full Name", max_length=50)
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(label="Phone Number", max_length=20)
    
    delivery_address = forms.CharField(
        label="Delivery Address",
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 20})
    )
    city = forms.CharField(label="City", max_length=20)
    postal_code = forms.CharField(label="Postal code", max_length=20)
    country = forms.CharField(label="Country", max_length=50)

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone_number', 'delivery_address', 
            'city', 'postal_code', 'country'
        ]