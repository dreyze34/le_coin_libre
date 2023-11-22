from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Image, Category, UserProfile, Order
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .form import AddProductForm, RegistrationForm, LoginForm, OrderProduct
from unidecode import unidecode
import os, shutil
import hashlib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def generer_chiffre_aleatoire_unique(string):
    # Utiliser SHA-256 pour créer un hachage unique
    hachage = hashlib.sha256(string.encode()).hexdigest()

    # Convertir le hachage en un nombre entier
    chiffre_aleatoire = int(hachage, 16)

    return chiffre_aleatoire

def index(request):
    template = loader.get_template('store/index.html')
    reserved_products = [Order.objects.all()[i].product for i in range(len(Order.objects.all()))]
    ordered_by_date_list = Product.objects.all().order_by('-date')
    unreserved_products = [ordered_by_date_list[i] for i in range(len(ordered_by_date_list)) if ordered_by_date_list[i] not in reserved_products]
    
    if unreserved_products :
        liste_produit = [
            {'nom':unreserved_products[i].title, 
            'prix':unreserved_products[i].price, 
            'description':unreserved_products[i].description,
            'user':unreserved_products[i].user.user.username,
            'date':unreserved_products[i].date, 
            'image': [
                unreserved_products[i].image_set.all()[j].image for j in range(len(unreserved_products[i].image_set.all()))
            ],
            'id':unreserved_products[i].id,}
            for i in range(len(unreserved_products))
        ]
        liste_categories = Category.objects.all()
        context = {'liste_produit': liste_produit, 'liste_categories': liste_categories}
        return render(request, 'store/index.html', context)
    else :
        context = {}
        return render(request, 'store/index.html', context)

def produit(request, id):
    template = loader.get_template('store/produit.html')
    product = Product.objects.get(id=id)
        
    Product_data = {
        'nom':product.title,
        'prix':product.price,
        'date':product.date, 
        'description':product.description,
        'id':product.id,
        'user':product.user.user.username,
        'image': [product.image_set.all()[i].image for i in range(len(product.image_set.all()))],
        'nb_image':len([product.image_set.all()[i].image for i in range(len(product.image_set.all()))])
        }
    context = {'Product': Product_data}
    return render(request, 'store/produit.html', context)

def order_product(request):
    print('test1')
    if request.method == 'POST':
        print('test')
        form = OrderProduct(request.POST)
        return render(request, 'store/order_product.html')
        print('test')
        product = Product.objects.get(id=id)
        reserved_products = [Order.objects.all()[i].product for i in range(len(Order.objects.all()))]   
        #if request.method == 'POST' :
        if request.user.is_authenticated and product not in reserved_products :
            order = Order.objects.create(product=product, buyer=request.user.userprofile)
            order.save()
    return redirect('index')

def handle_uploaded_file(file, i, destination_folder):
    
    original_filename, file_extension = os.path.splitext(file.name)
    filename = f'image{i+1}' + file_extension

    destination_path = os.path.join(destination_folder, filename)

    with open(destination_path, 'wb+') as destination :
        for chunk in file.chunks():
            destination.write(chunk)
    destination.close()

def copier_deplacer_image(chemin_source, chemin_destination, nouveau_nom):
    # Copier l'image du dossier source vers le dossier de destination
    shutil.copy(chemin_source, chemin_destination)

    # Construire le nouveau chemin complet avec le nouveau nom de fichier
    nouveau_chemin = os.path.join(chemin_destination, nouveau_nom)

    # Renommer le fichier dans le dossier de destination
    os.rename(os.path.join(chemin_destination, os.path.basename(chemin_source)), nouveau_chemin)

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
                product=Product(title=title, description=description, price=price, category=category, user = user.userprofile)
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

def search(request):
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
         'user':resultat[i].user.user.username,
         'date':resultat[i].date,
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
         'user':resultat[i].user.user.username,
         'date':resultat[i].date,
         'image': resultat[i].image_set.all()[0].image,
         'id':resultat[i].id}
        for i in range(len(resultat))
        ]
       
    else :
        liste_produit = []
    
    context = {'liste_produit' : liste_produit, 'liste_categories' : liste_categories}
    return render(request, 'store/recherche.html', context)

def disconnect(request):
    logout(request)
    return redirect('index')

#mathis.b@orange.fr
#bonjour123
#il faudra ajouter la vérification des mails centrale supélec et l'envoi de mail de confirmation
def auth(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            userp=UserProfile(user=user)
            userp.save()
            return redirect('index')  # Rediriger vers la page d'accueil ou toute autre page après l'inscription
    else:
        form = RegistrationForm()

    return render(request, 'store/register.html', {'form': form})
    
def connect(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')  # Rediriger vers la page d'accueil ou toute autre page après la connexion
    else:
        form = LoginForm()

    return render(request, 'store/login.html', {'form': form})

def a_propos(request):
    template = loader.get_template('store/a_propos.html')
    return render(request, 'store/a_propos.html')


def user_profile(request):
    reserved_products = [Order.objects.all()[i].product for i in range(len(Order.objects.all()))]
    username= request.GET.get("query", "")
    user = User.objects.filter(username = username)[0]
    userp = user.userprofile
    user_products = [userp.product_set.all()[i] for i in range(len(userp.product_set.all()))]
    unreserved_products = [userp.product_set.all()[i] for i in range(len(userp.product_set.all())) if userp.product_set.all()[i] not in reserved_products ]
    user_reserved_products = [reserved_products[i] for i in range(len(reserved_products)) if reserved_products[i] in userp.product_set.all()]
    images = Image.objects.filter(product__in=user_products)
    context = {'user': userp, 'reserved_products': user_reserved_products, 'unreserved_products': unreserved_products, 'images': images}
    template = loader.get_template('store/user_profile.html')
    return render(request, 'store/user_profile.html', context)

def delete_product(request, produit_id):
    produit = get_object_or_404(Product, id=int(produit_id))
    produit.delete()

    try:
        shutil.rmtree(f'./store/static/images/{produit_id}')
    except Exception as e:
        print(f"Erreur lors de la suppression du répertoire : {e}")
    
    return redirect(request.META.get('HTTP_REFERER'))
            
    
