from django.urls import path
from . import views

app_name= 'carte'


urlpatterns = [
    path('', views.carte , name='carte'),
]
