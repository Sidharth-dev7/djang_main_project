# forms.py
from django import forms
from .models import Customer,Garage

# -----------------------------------------------
#                   USER SECTION
# -----------------------------------------------

class AddForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'contact', 'email', 'password'] 

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
class EditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'contact', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# -----------------------------------------------
#                   GARAGE SECTION
# -----------------------------------------------

class GForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'services_offered': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }