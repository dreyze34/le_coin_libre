from django import forms
from .models import Product, Category
from django.forms.widgets import ClearableFileInput
from multiupload.fields import MultiFileField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AddProductForm(forms.ModelForm):
    title = forms.CharField(label="Titre")
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={'placeholder': 'Entrez une description du produit'}))  # Correction de la faute de frappe ici
    price = forms.DecimalField(label="Prix", widget=forms.NumberInput(attrs={'placeholder': 'Prix'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Catégorie")
    photos = MultiFileField(label="photos", required=False, min_num=0, max_num=10, max_file_size=1024*1024*5)
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']
    
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'Titre_ajout'})
        self.fields['description'].widget.attrs.update({'class': 'Description_ajout'})
        self.fields['price'].widget.attrs.update({'class': 'Prix_ajout'})
        self.fields['category'].widget.attrs.update({'class': 'Categorie_ajout'})
        self.fields['photos'].widget.attrs.update({'class': 'Photos_ajout'})

class OrderProduct(forms.ModelForm):
    pass


