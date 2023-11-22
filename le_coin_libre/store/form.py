from django import forms
from .models import Product, Category
from django.forms.widgets import ClearableFileInput
from multiupload.fields import MultiFileField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

#formulaire de création d'un utilisateur
# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(label="Adresse e-mail", required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

    
#forulaire de connexion d'un utilisateur
# class LoginForm(AuthenticationForm):
#     class Meta:
#         fields = ['username', 'password']

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

