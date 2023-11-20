from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('add_product/', views.add_product, name='add_product'),
    path('a_propos/',views.a_propos, name ='a_propos'),
    path('produit/<int:id>', views.produit, name= 'produit'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]