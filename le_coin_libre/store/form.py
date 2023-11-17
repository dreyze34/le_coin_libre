from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Category

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Adresse mail")
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']
    
class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Adresse mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
class AddProductForm(forms.ModelForm):
    title = forms.CharField(label="Titre")
    description = forms.CharField(label="Description")  # Correction de la faute de frappe ici
    price = forms.DecimalField(label="Prix", widget=forms.NumberInput(attrs={'step': '0.01'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']
