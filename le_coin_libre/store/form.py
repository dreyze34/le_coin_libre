from django import forms
from .models import Product, Category
from django.forms.widgets import ClearableFileInput



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

