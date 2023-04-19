from django.contrib.auth.models import User
from django.contrib.gis.db import models


def telecharger(instance , file_name):
    ext = file_name.split('.')[-1]
    username = instance.username
    return 'photo_profil/'+username+'.'+ext






class Membre(User):
    photo_profil = models.ImageField(verbose_name='photo de profil', upload_to=telecharger, blank=True)
    addresse =  models.CharField(max_length=100, verbose_name="addresse d'habitation", blank=True)
    tel = models.BigIntegerField(blank=True)
    profession = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(blank=True)
    is_driver = models.BooleanField(default=False)

    





