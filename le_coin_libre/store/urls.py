from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('add_product/', views.add_product, name='add_product'),
    path('auth/',views.auth, name ='auth'),
    path('a_propos/',views.a_propos, name ='a_propos'),
    path('produit/<int:id>', views.produit, name= 'produit'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path("connect/", views.connect, name='connect'),
    path(r'user_profile/', views.user_profile, name='user_profile'),
]