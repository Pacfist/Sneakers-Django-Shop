from django import forms
from .models import Order
from django.forms import ValidationError
import re
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
    
    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("Only numbers should be here")
        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Wrong phone number format. Wite only 10 numbers")
        
        return data
    
    def clean_email(self):
        data = self.cleaned_data['email']
    
    # Check if '@' is in the email
        if '@' not in data:
            raise forms.ValidationError("Invalid email format. Email must contain '@'.")
    
        return data


    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone_number', 'delivery_address', 
            'city', 'postal_code', 'country'
        ]