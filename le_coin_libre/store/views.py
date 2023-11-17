from django.shortcuts import render, redirect
from store.models import Product, Image, Category
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .form import CustomUserCreationForm
from unidecode import unidecode


def index(request):
    template = loader.get_template('store/index.html')
    ordered_list = Product.objects.all().order_by('-date')
    liste_produit = [
        {'nom':ordered_list[i].title, 'prix':ordered_list[i].price, 'description':ordered_list[i].description, 'image':Image.objects.get(product=ordered_list[i]).image}
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

def search(request):
    template = loader.get_template('store/recherche.html')
    search = unidecode(request.GET.get('search')).lower()
    catégorie = request.GET.get('Catégorie')
    liste_categories = Category.objects.all()

    if Product.objects.filter(normalized_title__icontains=search,  category = catégorie).exists() :
        resultat = Product.objects.filter(normalized_title__icontains=search,  category = catégorie)

    elif Product.objects.filter(normalized_title__icontains=search).exists() and int(catégorie) == 0 :
        resultat = Product.objects.filter(normalized_title__icontains=search)
       
    else :
        resultat = []
    
    context = {'liste_produit' : resultat, 'liste_categories' : liste_categories}
    return render(request, 'store/recherche.html', context)


def add_produit(request):




    template = loader.get_template('store/add_produit.html')
    return render(request, 'store/add_produit.html')

# def auth(request):
#     template = loader.get_template('store/authentification.html')
#     return render(request, 'store/authentification.html')

# def auth(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'Connexion réussie.')
#                 return redirect('index')  # Redirigez vers la page d'accueil ou toute autre page souhaitée
#             else:
#                 messages.error(request, 'Identifiant ou mot de passe incorrect.')
#     else:
#         form = CustomAuthenticationForm()

#     return render(request, 'auth.html', {'form': form})

def auth(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            form.instance.username = email
            user = authenticate(request, username=email,email=email, password=password)
            # if user is not None:
            #     login(request, user)
            #     messages.success(request, 'Connexion réussie.')
            #     messages.error(request, 'Identifiant ou mot de passe incorrect.')
            #     return redirect('index')
            # else:
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie.')
            return redirect('index')  # Redirigez vers la page d'accueil ou toute autre page souhaitée
                
    else:
        form = CustomUserCreationForm()

    return render(request, 'store/authentification.html', {'form': form})

def a_propos(request):
    template = loader.get_template('store/a_propos.html')
    return render(request, 'store/a_propos.html')
