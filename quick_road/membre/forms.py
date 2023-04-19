from django import forms 
from .models import Membre
from django.contrib.auth.forms import UserCreationForm

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ('username',
               # 'password1',
                'password',
                 'last_name',
                'first_name',
                'date_naissance',
                'photo_profil',
                
                'addresse',
                "tel",
                'email',
            )   
            

class MembrecreationForm(UserCreationForm):
    class Meta:
        model = Membre
        fields = ('username',
                'password1',
                'password2',
                 'last_name',
                'first_name',
                'date_naissance',
                'is_driver',  
                'photo_profil',
                'addresse',
                'tel',
                'email',
            )


            