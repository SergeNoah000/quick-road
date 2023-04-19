from django.db import models
from django.urls import reverse
from membre.models import  Membre




class PointField(models.Model):
    longitude = models.FloatField( null=True, blank=True)
    latitude = models.FloatField( null=True, blank=True)



class Vehicule(models.Model):
    type = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    etat = models.CharField(max_length=200, null=True, blank=True)
    nom = models.CharField(max_length=200, null=True, blank=True)
    nbre_place = models.IntegerField(default=5)


class Driver(Membre):
    car = models.OneToOneField(Vehicule, on_delete=models.CASCADE,related_name="driver", null=True, blank=True)
    date_acquisition= models.DateField(verbose_name="Date d'acquisition du vehicule", null=True, blank=True)

    def __init__(self, args, **kwargs):
        super.__init__(self,args, kwargs)
        self.is_driver = True

    


class Itineraire(models.Model):
    trouve = models.BooleanField(default=False)
    chemin = models.ForeignKey(PointField, on_delete=models.CASCADE,  null=True, blank=True)
    depart = models.CharField(max_length=200, null=True, blank=True)
    arrive = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField( auto_now_add=True)
    distance = models.FloatField( null=True, blank=True)
    temps = models.FloatField( null=True, blank=True)
    transport_mode = models.CharField(max_length=100, choices=[('foot', 'foot'), ('car', 'car'), ('train', 'train'), ], default='foot')



class SearchVehicule(models.Model):
    trouve = models.BooleanField(default=False)
    chemin = models.ForeignKey(PointField, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name="research_accepted", null=True, blank=True)
    depart = models.CharField(max_length=200, null=True, blank=True)
    arrive = models.CharField(max_length=200, null=True, blank=True)
    distance = models.FloatField( null=True, blank=True)
    temps = models.FloatField( null=True, blank=True)
    date = models.DateField( auto_now_add=True)
    montant = models.IntegerField(null=True, blank=True)
    transport_mode = models.CharField(max_length=100, choices=[('foot', 'foot'), ('car', 'car'), ('train', 'train'), ], default='foot')





class History(models.Model):
    membre = models.OneToOneField(Membre,related_name='history',  on_delete=models.CASCADE, null=True, blank=True)
    search_vehicule = models.ForeignKey(SearchVehicule, related_name="history", on_delete=models.CASCADE, null=True, blank=True)
    itineraire = models.ForeignKey(Itineraire, related_name="history", on_delete=models.CASCADE, null=True, blank=True,)





























# Create your models here.
class Measurement(models.Model):
    
    location = models.CharField( max_length=255)
    destination = models.CharField( max_length=255)
    created = models.DateTimeField( auto_now=False, auto_now_add=True)
    distance = models.DecimalField( max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"

    def __str__(self):
        return "The distance from {} to {} is mesures {}".format(self.location, self.destination, self.distance)

    def get_absolute_url(self):
        return reverse("Measurement_detail", kwargs={"pk": self.pk})
