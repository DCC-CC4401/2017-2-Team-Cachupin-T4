from django.contrib.auth.models import User, Permission
from django.db import models
from django.shortcuts import redirect


class Municipality(models.Model):
    name = models.TextField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    directions = models.TextField(max_length=200, null=True)
    avatar = models.ImageField(upload_to='municipality/avatar/', null=True, blank=True)

    def __str__(self):
        return self.name


class MunicipalityUser(models.Model):
    user = models.OneToOneField(User)
    municipality = models.ForeignKey('Municipality')

    def __str__(self):
        return self.municipality.name + " User"

    def get_index(self, request, context):
        return redirect('/municipality/')

    def save(self, *args, **kwargs):
        super(MunicipalityUser, self).save(*args, **kwargs)
        if not self.user.has_perm('municipality_user_access'):
            permission = Permission.objects.get(
                codename='municipality_user_access')
            self.user.user_permissions.add(permission)
        self.user.save()
