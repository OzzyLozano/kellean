from django.db import models
from django.contrib.auth.models import AbstractUser

class UserType(models.TextChoices):
    COMPRADOR = 'CMP','Comprador'
    VENDEDOR = 'VND','Vendedor'

class AppUser(AbstractUser):
    user_type = models.CharField(choices=UserType.choices,max_length=5)  
      
    def __str__(self):
        return self.username
    
    class Meta:
        permissions = (
            ('puede_vender','Puede vender y crear productos'),
            ('puede_comprar','Puede ver y comprar productos'),
        )