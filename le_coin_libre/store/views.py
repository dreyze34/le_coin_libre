from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Image, Category, Order
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .form import AddProductForm, OrderProduct
from unidecode import unidecode
from .form import AddProductForm
import os, shutil, hashlib, locale
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Transformation d'une adresse e-mail Centrale de la forme "prenom.nom@student-cs.fr" en "prenom nom"
def decomposer_nom_prenom(email):
    nom, prenom = email.split('.', 1)
    prenom = prenom.split('@')[0]
    nom = str.upper(nom[0])+nom[1:]
    prenom = str.upper(prenom[0])+prenom[1:]
    return nom + " " + prenom


# Gestion des fichiers téléversés lors de l'ajout d'un produit
def handle_uploaded_file(file, i, destination_folder):
    
    original_filename, file_extension = os.path.splitext(file.name)
    filename = f'image{i+1}' + '.jpg'

    destination_path = os.path.join(destination_folder, filename)

    with open(destination_path, 'wb+') as destination :
        for chunk in file.chunks():
            destination.write(chunk)
    destination.close()


# Copier/Renommer une image et la déplacer dans un autre dossier
def copier_deplacer_image(chemin_source, chemin_destination, nouveau_nom):
    # Copier l'image du dossier source vers le dossier de destination
    shutil.copy(chemin_source, chemin_destination)

    # Construire le nouveau chemin complet avec le nouveau nom de fichier
    nouveau_chemin = os.path.join(chemin_destination, nouveau_nom)

    # Renommer le fichier dans le dossier de destination
    os.rename(os.path.join(chemin_destination, os.path.basename(chemin_source)), nouveau_chemin)


# Retourne la liste des produits en page d'accueil
def index(request):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    template = loader.get_template('store/index.html')
    reserved_products = [Order.objects.all()[i].product for i in range(len(Order.objects.all()))]
    ordered_by_date_list = Product.objects.all().order_by('-date')
    unreserved_products = [ordered_by_date_list[i] for i in range(len(ordered_by_date_list)) if ordered_by_date_list[i] not in reserved_products]
    liste_categories = Category.objects.all()
    if unreserved_products :
        liste_produit = [
            {'nom':unreserved_products[i].title, 
            'prix':unreserved_products[i].price, 
            'description':unreserved_products[i].description,
            'user':unreserved_products[i].user.username,
            'date':unreserved_products[i].date.strftime("%A %d %B %Y").lower()+" à "+unreserved_products[i].date.strftime("%H:%M").lower(),
            'image': [
                unreserved_products[i].image_set.all()[j].image for j in range(len(unreserved_products[i].image_set.all()))
            ],
            'id':unreserved_products[i].id,
            'username': decomposer_nom_prenom(unreserved_products[i].user.username),}
            for i in range(len(unreserved_products))
        ]
        
        context = {'liste_produit': liste_produit, 'liste_categories': liste_categories}
        return render(request, 'store/index.html', context)
    else :
        context = {'liste_categories': liste_categories}
        return render(request, 'store/index.html', context)


# Retourne les caractéristiques d'un produit sur la page produit associée
def produit(request, id):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    template = loader.get_template('store/produit.html')
    product = Product.objects.get(id=id)
        
    Product_data = {
        'nom':product.title,
        'prix':product.price,
        'date':product.date.strftime("%A %d %B %Y").lower()+" à "+product.date.strftime("%H:%M").lower(), 
        'description':product.description,
        'id':product.id,
        'user':product.user.username,
        'image': [product.image_set.all()[i].image for i in range(len(product.image_set.all()))],
        'nb_image':len([product.image_set.all()[i].image for i in range(len(product.image_set.all()))])
        }
    context = {'Product': Product_data}
    return render(request, 'store/produit.html', context)


# Permet de réserver un produit
def order_product(request):

    if request.method == 'POST':
        product_id = int(request.POST.get("product_id"))
        product = Product.objects.get(id=product_id)
        reserved_products = [Order.objects.all()[i].product for i in range(len(Order.objects.all()))]

        if User.is_authenticated and product not in reserved_products :
            order = Order.objects.create(product=product, buyer=request.user)
            order.save()
        
        return redirect('index')
    
    else :
        return redirect('index')


# Permet de poster l'annonce d'un produit avec ses caractéristiques 
def add_product(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            form = AddProductForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                description=form.cleaned_data['description']
                price=form.cleaned_data['price']
                category=form.cleaned_data['category']
                username=request.user.username
                user = User.objects.filter(username=username)[0]
                product=Product(title=title, description=description, price=price, category=category, user = user)
                product.save()
                product_id=product.id
                list_photos = request.FILES.getlist('photos')

                if not list_photos :
                    destination_folder = f'./store/static/images/{product_id}'
                    os.makedirs(destination_folder, exist_ok=True)

                    copier_deplacer_image('./store/static/images/No-img.jpg', destination_folder, 'image1.jpg')

                    img = Image.objects.create(image=f'./static/images/{product_id}/image1', product=product)
                    img.save()

                if list_photos != [] :
                    destination_folder = f'./store/static/images/{product_id}'
                    os.makedirs(destination_folder, exist_ok=True)

                    for i in range(len(list_photos)):
                        handle_uploaded_file(list_photos[i], i, destination_folder)
                        img = Image.objects.create(image=f'./static/images/{product_id}/image{i+1}.jpg', product=product)
                        img.save()

                    return redirect('index')
        else:
            return redirect('connect')
    else:
        form = AddProductForm()

    return render(request, 'store/add_produit.html', {'form': form})


# Permet de rechercher un produit 
def search(request):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    template = loader.get_template('store/recherche.html')
    search = unidecode(request.GET.get('search')).lower()
    catégorie = request.GET.get('Catégorie')
    liste_categories = Category.objects.all()

    if Product.objects.filter(normalized_title__icontains=search,  category = catégorie).exists() :
        resultat = Product.objects.filter(normalized_title__icontains=search,  category = catégorie)
        liste_produit = [
        {'nom':resultat[i].title,
         'prix':resultat[i].price,
         'description':resultat[i].description,
         'user':resultat[i].user.username,
         'date':resultat[i].date.strftime("%A %d %B %Y").lower()+" à "+resultat[i].date.strftime("%H:%M").lower(),
         'image': resultat[i].image_set.all()[0].image,
         'id':resultat[i].id}
        for i in range(len(resultat))
        ]
         

    elif Product.objects.filter(normalized_title__icontains=search).exists() and int(catégorie) == 0 :
        resultat = Product.objects.filter(normalized_title__icontains=search)
        liste_produit = [
        {'nom':resultat[i].title,
         'prix':resultat[i].price,
         'description':resultat[i].description,
         'user':resultat[i].user.username,
         'date':resultat[i].date.strftime("%A %d %B %Y").lower()+" à "+resultat[i].date.strftime("%H:%M").lower(),
         'image': resultat[i].image_set.all()[0].image,
         'id':resultat[i].id}
        for i in range(len(resultat))
        ]
       
    else :
        liste_produit = []
    
    context = {'liste_produit' : liste_produit, 'liste_categories' : liste_categories}
    return render(request, 'store/recherche.html', context)


# Permet aux utilisateurs de se déconnecter de leur session
def disconnect(request):
    logout(request)
    return redirect('index')


# Création d'un nouvel utilisateur
def auth(request):
    form= UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    return render(request, 'store/register.html', {'form': form})
    
    
# Connexion d'un utilisateur
def connect(request):
    form= AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user= form.get_user()
            print(f"user: {user}")
            if user is not None :
                login(request, user)
                return redirect('index')
            else :
                messages.error(request, "Identifiants incorrects")         
    return render(request, 'store/login.html', {'form': form})



# Retourne les informations de la page "A propos" (contacts, service après vente...)
def a_propos(request):
    template = loader.get_template('store/a_propos.html')
    return render(request, 'store/a_propos.html')



# Retourne les informations de la page profil d'un utilisateur
def user_profile(request):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    reserved_products = [Order.objects.all()[i].product for i in range(len(Order.objects.all()))]
    username= request.GET.get("query", "")
    user = User.objects.filter(username=username)[0]
    userp_products = Product.objects.filter(user=user)
    user_reserved_products, unreserved_products = [], []
    for i in range(len(userp_products)):
        product_data = {
            'title': userp_products[i].title, 
            'price': userp_products[i].price, 
            'description': userp_products[i].description,
            'user': decomposer_nom_prenom(userp_products[i].user.username),
            'user_mail': userp_products[i].user.username,
            'date': userp_products[i].date.strftime("%A %d %B %Y").lower()+" à "+userp_products[i].date.strftime("%H:%M").lower(), 
            'image': [
            userp_products[i].image_set.all()[j].image for j in range(len(userp_products[i].image_set.all()))
            ],
            'id': userp_products[i].id,
            }
        if userp_products[i] in reserved_products :
            product_data['buyer'] = decomposer_nom_prenom(Order.objects.filter(product=userp_products[i])[0].buyer.username)
            product_data['buyer_mail'] = Order.objects.filter(product=userp_products[i])[0].buyer.username
            user_reserved_products.append(product_data)

        else :
            unreserved_products.append(product_data)
    
    
    context = {'username': decomposer_nom_prenom(user.username), 'email':user.username, 'reserved_products': user_reserved_products, 'unreserved_products' : unreserved_products}
    template = loader.get_template('store/user_profile.html')
    return render(request, 'store/user_profile.html', context)



# Supprimer un produit ainsi que son répertoire d'image(s) associé
def delete_product(request, produit_id):
    produit = get_object_or_404(Product, id=int(produit_id))
    produit.delete()


    try:
        shutil.rmtree(f'./store/static/images/{produit_id}')
    except Exception as e:
        print(f"Erreur lors de la suppression du répertoire : {e}")
    
    return redirect(request.META.get('HTTP_REFERER'))
            
    
