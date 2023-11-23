# Clonage et exécution 
* Cloner le répertoire distant avec git.

* Vérifier que _unidecode_ et _multiupload_ sont bien installées sur VSCode.  
Sinon, les importer comme suit :

``` 
pip install unidecode
pip install django-multiupload
``` 

* Se positionner dans le bon répertoire (./le_coin_libre_2/le_coin_libre/).

* Exécuter le code suivant dans le terminal pour accéder à l'application Web : 
```
python manage.py runserver  

```
&nbsp;

# Model-View-Presenter  
Site de vente/achat en ligne fonctionnel comprenant :

**1.** Un système d'authentification  
**2.** Un système d'ajout de produits relié à un catalogue   
**3.** Une interface utilisateur recensant les produits vendus et achetés pour chaque utilisateur  
**4.** La possibilité de rechercher des produits (catégories, mots clés)  
**5.** Initialement une communication entre acheteurs et vendeurs a été réalisée à l'aide des coordonnées      téléphoniques. Celles-ci étant renseignées dans les profils utilisateurs.  
**6.** Finalement, un système de chat a été mis en place. Pour chaque produit, les utilisateurs peuvent échanger directement sur la plateforme de l'application.  

&nbsp;
&nbsp;


# Model-View-Controller 
Pour cette partie, nous faisons appel au modèle User.
Nous l'importons depuis Django de la manière suivante :

```
from django.contrib.auth import User

```


## Fonctionnalités 

### Authentification 
- **Modèle** (_models.py - User_): le modèle User gère les informations liées aux utilisateurs (mot de passe, email ...).

- **Vue** (_views.py - auth, connect_): les fonctions de vue 'auth' et 'connect' gèrent respectivement l'inscription et la connexion des utilisateurs.

- **Contrôleur** (_urls.py_): les URLs associées redirigent vers les fonctions de vue appropriées (auth, connect).



### Ajout d'un Produit 
- **Modèle** (_models.py - Product et User_): Le modèle Product représente un produit (dont les images du modèle Image et la catégorie du modèle Category associées à ce produit) et le modèle User représente l'utilisateur qui ajoute ce produit (connexion nécessaire pour ajouter un produit)

- **Vue** (_views.py - add product_): La fonction de vue add_product gère la logique d'ajout d'un produit en utilisant le formulaire AddProductForm.

- **Contrôleur** (_urls.py_): L'URL associée à l'ajout d'un produit dirige la requête vers la fonction de vue appropriée (add_product).



### Suppression d'un Produit 
- **Modèle** (_models.py - Product et User_): le modèle User représente l'utilisateur qui supprime un produit (la suppression est permise uniquement par l'utilisateur ayant ajouté le produit).

- **Vue** (_views.py - delete product_) : La fonction de vue delete_produit permet de supprimer un produit.

- **Contrôleur** (_urls.py_): l'URL associée à la suppresion d'un produit dirige la requête vers la fonction de vue appropriée (delete_product).



### Commande d'un Produit 
- **Modèle** (_models.py - Order_): Le modèle Order est une classe comprenant des détails sur un produit commandé : le produit, l'acheteur et la date d'achat.

- **Vue** (_views.py - order product_): La fonction de vue order_product gère la logique de commande d'un produit en créant une nouvelle commande dans le modèle Order.

- **Contrôleur** (_urls.py_): L'URL associée à la commande d'un produit dirige la requête vers la fonction de vue appropriée (order_product).



### Affichage d'un Produit 
- **Modèle** (_models.py - Product_): le modèle contient les caractéristique d'un produit et affiche l'image et le vendeur associés (relations avec le modèle Image et User).

- **Vue** (_views.py - produit_): La fonction de vue produit récupère les caractéristiques du produit à afficher.

- **Contrôleur** (_urls.py_): L'URL associée à l'affichage d'un produit dirige la requête vers la fonction de vue appropriée (produit).



### Recherche 
- **Modèle** (_models.py - Product, Catégorie_): Le modèle Product représente les produits recherchés et le modèle Category, les différentes catégories triant les produits. 

- **Vue** (_views.py - search_): la fonction de vue search gère la logique de recherche en filtrant les produits en fonction des critères de recherche.

- **Contrôleur** (_urls.py_): L'URL associée à la recherche dirige la requête vers la fonction de vue appropriée (search).



### Page d'accueil 
- **Modèle** (_models.py - Product_): la classe représente les produits avec des caractéristiques spécifiques tels que le titre, la description, le prix, la date, l'utilisateur (ainsi que la catégorie et images associées)

- **Vue** (_views.py - index_): la fonction de vue index gère la logique de présentation de la page d'accueil en récupérant les produits non réservés depuis le modèle.

- **Contrôleur** (_urls.py_): L'URL associée à la page d'accueil dirige la requête vers la fonction de vue appropriée (index).



### Déconnexion 
- **Modèle** : Non concerné.

- **Vue** (_views.py - disconnect_): La fonction de vue disconnect gère la logique de déconnexion.

- **Contrôleur** (_urls.py_): L'URL associée à la déconnexion dirige la requête vers la fonction de vue appropriée (disconnect).



### Chat 
- **Modèle** (_models.py - Room, Message_): La classe Room représente une salle de discussion.  La classe Message stocke les messages envoyés, associant chaque message à un utilisateur, une salle, et contenant le texte du message ainsi que la date d'envoie. 

- **Vue** (_views.py - home, room, checkview, send, getMessage_): La fonction home rend la page d'accueil avec la liste des conversations et des utilisateurs qui y sont impliqués. La fonction room rend la page d'une salle de chat, ses détails et ses messages. La fonction checkview redirige vers une salle de discussion existante, et dans le cas contraire, elle dirige vers une nouvelle salle qui vient d'être créée. La fonction send renvoie une réponse indiquant que le message a été envoyé. La fonction getMessages renvoie les messages d'une salle.

- **Contrôleur** (_urls.py_): les URLs associées redirigent vers les fonctions de vue appropriées (home, room, checkview, send, getMessage).

&nbsp;
&nbsp;


# Cas d'usage 
## Première connexion/inscription 
L'utilisateur renseigne _adresse mail_, _username_, _password_.  
## Connexion  
L'utilisateur renseigne _username_ et _password_.  
## Mise en vente d'un produit 
L'utilisateur saisit un titre et une description. Il choisit également une catégorie, un prix. La date ainsi que le nom du vendeur sont renseignés automatiquement.  
## Achat d'un produit 
L'utilisateur peut être directement intéressé par un produit présent sur la page d'acceuil.  
Il peut également rechercher un produit spécifique grâce à la barre de recherche et/ou un choix de catégorie.  
## Échanges avec d'autres utilisateurs 
Les utilisateurs peuvent demander puis recevoir des renseignements à propos d'un produit via un chat.  
En particulier, cela favorise la communication entre les acheteurs et les vendeurs pour conclure quant au paiement du produit.  
## Consultation des produits mis en vente et évolution des status
Les vendeurs peuvent suivre en temps réel l'évolution des status des annonces qu'ils postent en ligne.  
 Il leur suffit de consulter leur _Profil Utilisateur_. Ils peuvent également supprimer des produits qu'ils ne souhaitent plus vendre.  
 De manière analogue il est possible, pour les utilisateurs, de consulter sur le même profil les produits qu'ils ont réservé/acheté.  
 Afin de répondre aux exigences de confidentialité, les vendeurs ne modifient uniquement que les produits qu'ils proposent en ligne.

&nbsp;
&nbsp;


# Feuille de route 

|Jour | Actions | 
|-------|----------|
|**15/11**|Choix du projet : Le Coin Libre, création du diagramme entité-association associé et du dépôt gitlab. Sur papier, création de templates en vue d'une implémentation en CSS/HTML.         | 
|**16/11**| Début de création du templates commun à toutes les views (header/footer, couleurs, polices).   Création de la page d'accueil (voir store/index), des classes utilisées (voir store/models; à modifier tout au long des fonctionnalités) |
|**17/11**   &nbsp;&nbsp;&nbsp;&nbsp;  | Début/Fin des views à propos. Début views authentification/add_product. Test ajout d'objets aux classes (user, product ...) |    
|**20/11**| Fin add_product/authentication. Début user_profil. Début/Fin product.|
|**21/11**| Trois membres au Forum tandis que trois autres achèvent la page _user profile_. Vérification de la mise en relation des différentes fonctions : add_product/product/profil/index.|
|**22/11** | Préparation de la présentation (Latex). Début des fonctionnalités Chat et Order.|
|**23/11**| Fin de la présentation. Finalisation des fonctionnalités et travail sur l'esthétique du site.| 
|**24/11**| Répétitions avant passage.|

&nbsp;
&nbsp;

# Fonctionnalités complétées  
## Toutes les fonctions apparaissent dans _store/views.py_

* Page d'acceuil (cf _index_)
* Recherche (cf _search_)
* Authentification/connexion (cf _auth_, _connect_, _disconnect_) 
* Page utilisateur (cf _user profile_)
* Achat
* Ajout/suppression de produit(s) (cf _add product_; _delete product_)
* Page produit (cf _produit_)
* page à propos (cf _a propos_)
* Onglet _Messagerie_ (cf _chat_)
