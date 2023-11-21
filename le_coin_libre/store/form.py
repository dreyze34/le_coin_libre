from django import forms
from .models import Product, Category
from django.forms.widgets import ClearableFileInput
from multiupload.fields import MultiFileField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



#formulaire de création d'un utilisateur
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Adresse mail")
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']
    
#forulaire de connexion d'un utilisateur
class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Adresse mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

#formulaire d'ajout d'un produit
class AddProductForm(forms.ModelForm):
    title = forms.CharField(label="Titre")
    description = forms.CharField(label="Description")  # Correction de la faute de frappe ici
    price = forms.DecimalField(label="Prix")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Catégorie")
    photos = MultiFileField(label="photos", required=False, min_num=0, max_num=10, max_file_size=1024*1024*5)
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']

