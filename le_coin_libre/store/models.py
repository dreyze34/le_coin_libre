from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from unidecode import unidecode
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    normalized_name=models.CharField(max_length=200, default="default")
    def save(self, *args, **kwargs):
        self.normalized_name = unidecode(self.name).lower()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today())
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    normalized_title=models.CharField(max_length=200, default="default")
    def save(self, *args, **kwargs):
        self.normalized_title = unidecode(self.title).lower()
        super().save(*args, **kwargs)
    
class Image(models.Model):
    image = models.ImageField(upload_to='static/images/',default='static/images/No-img.jpg')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)