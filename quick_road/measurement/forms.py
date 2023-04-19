from django.forms import ModelForm, models
from .models import Measurement, SearchVehicule, Itineraire

class MeasurementForm(models.ModelForm):
    class Meta:
        model = Measurement
        
        fields = ('destination','location')




class ItineraireForm(ModelForm):
    class Meta:
        model = Itineraire
        fields = (
               'depart',
               'arrive',
               'transport_mode'
              
            )   
            
class SearchVehiculeForm(ModelForm):
    class Meta:
        model = SearchVehicule
        fields = (
               'depart',
               'arrive',
               'montant'
              
            )   
            
