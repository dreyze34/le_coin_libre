from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('add_product/', views.add_produit, name='add_produit'),
    path('auth/',views.auth, name ='auth'),
    path('a_propos/',views.a_propos, name ='a_propos'),
]