from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import Membre, MembreForm, MembrecreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = MembrecreationForm(request.POST, request.FILES)
        if form.is_valid():
                user = form.save(commit=False)
                user.save()
                return redirect('carte:carte')
                
        else:
            for error in form.errors:
                print(error)                    
            return HttpResponse("<h2><strong class='text-center' > FORMULAIRE NON VALIDE, VERIFIE ET REVIENTS VOIR</strong></h2>")
    else:
        form = MembrecreationForm( )
        return render(request, 'membre/register.html', {'form':form})
            

def login_membre(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) 
        print(type(user))
        login(request, user)
        
        return redirect('carte:carte')
    
    else:
        return render(request, 'membre/login.html')


def logout_membre(request):
    logout(request)
    return redirect('membre:login')


@login_required
def update_membre(request, id):
    if request.user.id == id:
        if request.method == 'POST':
            form = MembrecreationForm(request.POST, request.FILES, instance=request.user.membre)
            if form.is_valid():
                    user = form.save(commit=False)
                    user.save()
                    return redirect('membre:detail', kwargs={'id':user.id} )               
            else:
                for error in form.errors:
                    print(error)                    
                return HttpResponse("<h2><strong class='text-center' > FORMULAIRE NON VALIDE, VERIFIE ET REVIENTS VOIR</strong></h2>")
        else:
            form = MembrecreationForm( instance=request.user.membre)
            return render(request, 'membre/update_membre.html', {'form':form, 'membre':request.user.membre})


@login_required
def membre_detail(request, id=0):
    if id == 0:
        membre = request.user.membre
        return render (request, 'membre/details_membre.html', {'membre':membre})
    else:
        membre = User.objects.get(id=id)
        return render (request, 'membre/details_membre.html', {'membre':membre})
   
        