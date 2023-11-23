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
    path('connect/', views.connect, name='connect'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('delete_product/<int:produit_id>/', views.delete_product, name='delete_product'),
    path('order_product/', views.order_product, name='order_product'),
    path('chat', views.home , name ="home"),
    path('<str:room>/', views.room , name ="room"),
    path('checkview', views.checkview , name ="checkview"),
    path('send', views.send , name ="send"),
    path('getMessages/<str:room>/', views.getMessages , name ="getMessages")

]

