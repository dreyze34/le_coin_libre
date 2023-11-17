from django.db import models
from datetime import date
from django.contrib.auth.models import User
from unidecode import unidecode

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # mail = models.EmailField(max_length=300, unique=True)
    # password = models.CharField(max_length=200)
    # phone = models.CharField(max_length=10)
    
class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    normalized_title=models.CharField(max_length=200, default="default")
    def save(self, *args, **kwargs):
        self.normalized_title = unidecode(self.title).lower()
        super().save(*args, **kwargs)
    
class Image(models.Model):
    image = models.ImageField(upload_to='static/images/',default='static/images/No-img.jpg')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)