from unicodedata import name
from django.urls import path
from . import views

app_name  = 'membre'

urlpatterns = [
    path('register/', views.register ,name='register'),
    path('login/', views.login_membre, name="login"),
    path("logout/", views.logout_membre, name="logout"),
    path('detail/<int:id>', views.membre_detail, name='detail'),
    path('update/<int:id>/', views.update_membre, name="update" ),


]
