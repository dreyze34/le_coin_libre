from django.shortcuts import render, redirect
from store.models import Product, Image, Category
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .form import CustomUserCreationForm
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import AddProductForm, CustomAuthenticationForm
import os
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
        {'nom':ordered_list[i].title, 'prix':ordered_list[i].price, 
        'description':ordered_list[i].description, 
        'image': Image.objects.values_list('image', flat=True).filter(product= ordered_list[i])[0],
        'id':ordered_list[i].id,}
        for i in range(len(ordered_list))
    ] 
    liste_categories = Category.objects.all()
    context = {'liste_produit': liste_produit, 'liste_categories': liste_categories}
    return render(request, 'store/index.html', context)

def produit(request, id):
    template = loader.get_template('store/produit.html')
    product = Product.objects.get(id=id)
    liste_produit = {
        'nom':product.title,
        'prix':product.price, 
        'description':product.description,
        'image': [product.image_set.all()[i].image for i in range(len(product.image_set.all()))],
        'nb_image':len([product.image_set.all()[i].image for i in range(len(product.image_set.all()))])
        }
    print(len(product.image_set.all()))
    context = {'liste_produit': liste_produit}
    return render(request, 'store/produit.html', context)

def handle_uploaded_file(file, i, product_id):
    destination_folder = f'./static/images/{product_id}'

    os.makedirs(destination_folder, exist_ok=True)

    original_filename, file_extension = os.path.splitext(file.name)
    filename = f'image{i}' + file_extension

    destination_path = os.path.join(destination_folder, filename)

    with open(destination_path, 'wb+') as destination :
        for chunk in file.chunks():
            destination.write(chunk)
    destination.close()

def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:                
                product = form.save(commit=False)
                # Associer le produit à l'utilisateur actuel
                product.user = request.user
                product.save()
                product_id = product.id
                list_photos = request.FILES.getlist('photos')

                for i in range(len(list_photos)):
                    handle_uploaded_file(list_photos[i], i, product_id)

                for i in range(len(list_photos)):
                    img = Image.objects.create(image=f'./static/images/{product_id}/image{i}', product=product)
                    img.save()

                return redirect('index')
            else:
                return redirect('connect')
    else:
        form = AddProductForm()

    return render(request, 'store/add_produit.html', {'form': form})

def search(request):
    template = loader.get_template('store/recherche.html')
    search = unidecode(request.GET.get('search')).lower()
    catégorie = request.GET.get('Catégorie')
    liste_categories = Category.objects.all()

    if Product.objects.filter(normalized_title__icontains=search,  category = catégorie).exists() :
        resultat = Product.objects.filter(normalized_title__icontains=search,  category = catégorie)
        liste_produit = liste_produit = [
        {'nom':resultat[i].title, 'prix':resultat[i].price, 'description':resultat[i].description, 'image': resultat[i].image_set.all()[0].image}
        for i in range(len(resultat))
        ]
        print(resultat[0].image_set.all()[0].image)
         

    elif Product.objects.filter(normalized_title__icontains=search).exists() and int(catégorie) == 0 :
        resultat = Product.objects.filter(normalized_title__icontains=search)
        liste_produit = liste_produit = [
        {'nom':resultat[i].title, 'prix':resultat[i].price, 'description':resultat[i].description, 'image': resultat[i].image_set.all()[0].image}
        for i in range(len(resultat))
        ]
        print(resultat[0].image_set.all()[0].image)
       
    else :
        liste_produit = []
    
    context = {'liste_produit' : liste_produit, 'liste_categories' : liste_categories}
    return render(request, 'store/recherche.html', context)

#mathis.b@orange.fr
#bonjour123
#il faudra ajouter la vérification des mails centrale supélec et l'envoi de mail de confirmation

def disconnect(request):
    logout(request)
    redirect('index')
    return redirect('index')

def a_propos(request):
    template = loader.get_template('store/a_propos.html')
    return render(request, 'store/a_propos.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            login(request, user)
            return redirect('index')  # Remplacez 'home' par le nom de votre vue d'accueil
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('index')  # Remplacez 'home' par le nom de votre vue d'accueil
#     else:
#         form = AuthenticationForm()
#     return render(request, 'store/login.html', {'form': form})



def user_login(request):
    print("a")
    if request.method == 'POST':
        print("b")
        form = CustomAuthenticationForm(request, data=request.POST)
        print("c")
        print(form.errors)
        print(form.data)
        if form.is_valid():
            print("d")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            print("e")
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # Utilisateur non authentifié - Gérer cela selon vos besoins
                print('Adresse e-mail ou mot de passe incorrect.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'store/login.html', {'form': form})