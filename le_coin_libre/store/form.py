from django import forms
from .models import Product, Category
from django.forms.widgets import ClearableFileInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class CustomUserCreationForm(UserCreationForm):
     email = forms.EmailField()
     phone_number = forms.CharField(max_length=15, required=False)
     class Meta:
        model = CustomUser
        fields = ['email', 'phone_number']



#formulaire d'ajout d'un produit
class AddProductForm(forms.ModelForm):
    title = forms.CharField(label="Titre")
    description = forms.CharField(label="Description")  # Correction de la faute de frappe ici
    price = forms.DecimalField(label="Prix")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Catégorie")
    photos = forms.FileField(label="Photos", required=False, widget=forms.ClearableFileInput())
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']

