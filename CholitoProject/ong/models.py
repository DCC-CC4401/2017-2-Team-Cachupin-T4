from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.


class ONG(models.Model):
    name = models.TextField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    directions = models.TextField(max_length=200, null=True)
    avatar = models.ImageField(upload_to='ong/avatar/')
    
    def __str__(self):
        return self.name


class ONGUser(User):
    ong = models.ForeignKey('ONG')
