from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product, Image, Category, UserProfile
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .form import AddProductForm
from unidecode import unidecode
import os, shutil
import hashlib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def generer_chiffre_aleatoire_unique(string):
    # Utiliser SHA-256 pour créer un hachage unique
    hachage = hashlib.sha256(string.encode()).hexdigest()

    # Convertir le hachage en un nombre entier
    chiffre_aleatoire = int(hachage, 16)

    return chiffre_aleatoire

def index(request):
    template = loader.get_template('store/index.html')
    ordered_list = Product.objects.all().order_by('-date')

    if ordered_list :
        liste_produit = [
            {'nom':ordered_list[i].title, 
            'prix':ordered_list[i].price, 
            'description':ordered_list[i].description, 
            'image': [
                ordered_list[i].image_set.all()[j].image for j in range(len(ordered_list[i].image_set.all()))
            ],
            'id':ordered_list[i].id,}
            for i in range(len(ordered_list))
        ]
        print(ordered_list[1].image_set.all()[0].image)
        liste_categories = Category.objects.all()
        context = {'liste_produit': liste_produit, 'liste_categories': liste_categories}
        return render(request, 'store/index.html', context)
    else :
        context = {}
        return render(request, 'store/index.html', context)

def produit(request, id):
    template = loader.get_template('store/produit.html')
    product = Product.objects.get(id=id)
    liste_produit = {
        'nom':product.title,
        'prix':product.price, 
        'description':product.description,
        'id':product.id,
        'image': [product.image_set.all()[i].image for i in range(len(product.image_set.all()))],
        'nb_image':len([product.image_set.all()[i].image for i in range(len(product.image_set.all()))])
        }
    context = {'liste_produit': liste_produit}
    return render(request, 'store/produit.html', context)

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
        form = AddProductForm(request.POST)
        if form.is_valid():               
            product = form.save(commit=False)
            # Associer le produit à l'utilisateur actuel
            product.save()
            product_id = product.id
            list_photos = request.FILES.getlist('photos')
            print(list_photos)

            if not list_photos :
                destination_folder = f'./store/static/images/{product_id}'
                os.makedirs(destination_folder, exist_ok=True)

                copier_deplacer_image('./store/static/images/No-img.jpg', destination_folder, 'image1.jpg')

                img = Image.objects.create(image=f'./static/images/{product_id}/image1', product=product)
                img.save()

            if list_photos != [] :
                print('test')
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



def disconnect(request):
    logout(request)
    redirect('index')
    return redirect('index')

#mathis.b@orange.fr
#bonjour123
#il faudra ajouter la vérification des mails centrale supélec et l'envoi de mail de confirmation
def auth(request):
    form= UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    return render(request, 'store/register.html', {'form': form})
    
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


def a_propos(request):
    template = loader.get_template('store/a_propos.html')
    return render(request, 'store/a_propos.html')

@login_required
def user_profile(request):
    a= request.GET.get("query", "")
    b = User.objects.filter(email = a)[0]
    user_data = b.userprofile
    product_data = user_data.product_set.all()
    image_data = Image.objects.filter(product__in=product_data)
    context = {'user_data': user_data, 'product_data': product_data, 'image_data': image_data}
    template = loader.get_template('store/user_profile.html')
    return render(request, 'store/user_profile.html', context)

def product_delete(request):
    product_data = Product.objects.filter(user=request.user)
    product_data.delete()
    return render(request, 'store/user_profile.html')
