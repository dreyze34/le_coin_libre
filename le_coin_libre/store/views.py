from django.shortcuts import render, redirect
from store.models import Product, Image, Category, UserProfile
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .form import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .form import AddProductForm
from unidecode import unidecode
import hashlib

def generer_chiffre_aleatoire_unique(string):
    # Utiliser SHA-256 pour créer un hachage unique
    hachage = hashlib.sha256(string.encode()).hexdigest()

    # Convertir le hachage en un nombre entier
    chiffre_aleatoire = int(hachage, 16)

    return chiffre_aleatoire

def index(request):
    template = loader.get_template('store/index.html')
    ordered_list = Product.objects.all().order_by('-date')
    liste_produit = [
        {'nom':ordered_list[i].title, 'prix':ordered_list[i].price, 'description':ordered_list[i].description, 'image': Image.objects.values_list('image', flat=True).filter(product= ordered_list[i])[0]}
        for i in range(len(ordered_list))
    ] 
    liste_categories = Category.objects.all()
    context = {'liste_produit': liste_produit, 'liste_categories': liste_categories}
    return render(request, 'store/index.html', context)

def produit(request):
    template = loader.get_template('store/produit.html')
    product_list = Product.objects.all()
    liste_produit = [
        {'nom':product_list[i].title, 'prix':product_list[i].price, 'description':product_list[i].description,
         'image': Image.objects.filter(product= product_list[i])[0].image}
        for i in range(len(product_list))
    ] 
    context = {'liste_produit': liste_produit}
    return render(request, 'store/produit.html', context)

def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                
                product = form.save(commit=False)
                # Associer le produit à l'utilisateur actuel
                product.user = request.user
                product.save()
                photos = request.FILES.getlist('photos') 
                for photo in photos:
                    Image.objects.create(image=photo, product=product)
                return redirect('index')
            else:
                return redirect('connect')
    else:
        form = AddProductForm()

    return render(request, 'store/add_produit.html', {'form': form})


def search(request):
    template = loader.get_template('store/recherche.html')
    search = unidecode(request.GET.get('search')).lower()
    catégorie = request.GET.get('Categorie')
    liste_categories = Category.objects.all()

    if Product.objects.filter(normalized_title__icontains=search,  category = catégorie).exists() :
        resultat = Product.objects.filter(normalized_title__icontains=search,  category = catégorie)

    elif Product.objects.filter(normalized_title__icontains=search).exists() and int(catégorie) == 0 :
        resultat = Product.objects.filter(normalized_title__icontains=search)
       
    else :
        resultat = []
    
    context = {'liste_produit' : resultat, 'liste_categories' : liste_categories}
    return render(request, 'store/recherche.html', context)

#mathis.b@orange.fr
#bonjour123
#il faudra ajouter la vérification des mails centrale supélec et l'envoi de mail de confirmation
def auth(request):
    
    print("post")
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = form.save()
        user.id = generer_chiffre_aleatoire_unique(email)
        user.save()
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('index')
                
    

    return render(request, 'store/authentification.html', {'form': form})

def a_propos(request):
    template = loader.get_template('store/a_propos.html')
    return render(request, 'store/a_propos.html')


def disconnect(request):
    logout(request)
    redirect('index')
    return redirect('index')

def connect(request): 
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Définissez le champ 'username' avec la valeur de l'email
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else :
                messages.error(request, 'Identifiant ou mot de passe incorrect.')
                
    else:
        form = CustomAuthenticationForm(request.POST)
    
    return render(request, 'store/authentification.html', {'form': form}) 
