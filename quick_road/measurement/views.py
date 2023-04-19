from django.shortcuts import render
import folium 
from .models import PointField, History, Driver
from django.contrib import messages
from geopy.geocoders import Nominatim
from pyroutelib3 import Router
from geopy.distance import geodesic
from .forms import SearchVehiculeForm, Itineraire, SearchVehicule, ItineraireForm


def get_center_cooordinates(laA:float,loA:float,laB:float=None,loB:float=None):
    coords = (laA, loA)
    if laB:
        coords1 =(laA+loA)/2
        coords2 = (loB+loB)/2
        
        return (coords1, coords2)
    
    
def get_zoom(distance): 
    if(25<distance):
        return 8
    

    if(25<distance<100):
        return 6
    
    elif(100<distance and distance<500):
        return 4
    
    else:
        return 2 
    
    
# Create your views here.
def carte(request):
    #class de geopy qui permet de retrouver les lieux saisies ou les addresses ip 
    helper = Nominatim(user_agent="carte")

    #point de depart ou va etre centre la carte sans le formulaire de recherche
    point = helper.geocode("total melen yaoundé")
    distance =0.0
    temps=0.0

    #Initialisation de la carte 
    carte = folium.Map(width=820, height=1110, location = (point.latitude, point.longitude), zoom_start=2)
    
    #formaulaire de recherche de taxima
    form1 = SearchVehiculeForm(request.POST or None)
    form =ItineraireForm(request.POST or None)

        
    if form.is_valid():
        instance = form.save(commit=False)
        location = helper.geocode(instance.depart)
        destination = helper.geocode(instance.arrive)
    
        print("location:" , location)
        print("\n destination: ", destination)
        
        pointA = (location.latitude, location.longitude)
        pointB = (destination.latitude, destination.longitude)

        distance = geodesic(pointA, pointB)
        carte  = folium.Map(width=700, height=700, center=get_center_cooordinates(location.latitude, location.longitude, destination.latitude, destination.longitude), zoom_start=14)      
       
        folium.Marker(location=pointA, tooltip = 'depart', popup=location,
                    icon=folium.Icon(color='blue', icon='cloud')).add_to(carte)
        
        #destination's markers  initialization
        folium.Marker(location=pointB, tooltip = 'destination', popup=destination,
                    icon=folium.Icon(color='green', icon='cloud')).add_to(carte)

        router = Router(instance.transport_mode)

        depart = router.findNode(location.latitude, location.longitude)
        print("\ndepart:", depart)
        arrivee = router.findNode(destination.latitude,  destination.longitude)
        print("\narrive: ", arrivee)


        status, route = router.doRoute(depart, arrivee)
        if status == 'success':
            print("route trouvée ")
            routeLatLons = list(map(router.nodeLatLon, route))
        else:
            print("route pas trouvée !")
            messages.add_message(request, messages.INFO, 'La destination ou le depart ne sont pas connus de notre base de donnes <p><u><h4>Note</h4></u> ESSAYER UN NOM UNIVERSEL DES LIEUX</p>')
            
        print(routeLatLons)

        #recuperation des coordonnees de l'itineraire et calcul de la longueur de l'itineraire
        distance = 0.0
        point = PointField.objects.create(latitude= routeLatLons[0][0], longitude=routeLatLons[0][0])
        point.save()
        instance.chemin =point
        for i in range(len(routeLatLons)):
            coord=list(routeLatLons[i])
            
            #ajout des elements pour l'historique
            point = PointField(latitude=coord[0], longitude=coord[1])
            point.save()
            instance.chemin.add= point
                
            
            #ajout du point sur la carte en vu du tracage de l'itineraire 
            if i!=0:
                distance += round( geodesic(list(routeLatLons[i-1]), list(routeLatLons[i])).km, 2)
            folium.CircleMarker(coord,radius = 3,fill=True, color='red' , opacity=0.5).add_to(carte)
            
            #ajout des point de l'intineraire sur la carte
        folium.PolyLine(routeLatLons, color="blue", weight=2.5, opacity=1).add_to(carte)
        
        
        #ajout des lignes entre les differents point de l'itineraire 
        #sudline = folium.PolyLine(locations=[pointA, pointB], width=7, color='green')
        ##carte.add_child(sudline)
        temps = distance*1000/3 
        temps = temps/60 + temps%60       
        instance.distance = distance
        instance.temps = temps
        instance.trouve = True
        instance.save()
       # obj, created = History.objects.get_or_create(membre = request.user.membre)
        #obj.itineraire.add(instance)
        routeLatLons=[pointA,pointB]
        carte = carte._repr_html_()
        research = SearchVehicule.objects.all()
        context = {
            'carte':carte,
            'distance':distance, 
            'temps':temps,
            'form_itineraire': form,
            'form1':form1,
            'researchs': research,
        }
        return render(request, 'measurement/carte.html', context)

    if form1.is_valid():
        instance = form1.save(commit=False)

       
        membre = request.user.membre
        hist , created = History.objects.get_or_create(membre=membre)
        instance.save()
        hist.search_vehicule =instance
        hist.save()
        research = SearchVehicule.objects.all()
        context = {
                'carte':carte,
                'distance':distance, 
                'temps':temps,
                'form_itineraire': form,
                'form1':form1,
                'researchs': research,
            }
        return render(request, 'measurement/carte.html', context)

        if request.method == "POST" and request.POST['accept_rechearch']:
            search =SearchVehicule.objects.get(id=int(request.POST['id']))
            driver = Driver.objects.get(id=int(request.POST['id_driver']))
            search.driver = driver
            search.save()
            carte = carte._repr_html_()
            research = SearchVehicule.objects.all()
            context = {
                'carte':carte,
                'distance':distance, 
                'temps':temps,
                'form_itineraire': form,
                'form1':form1,
                'researchs': research,
            }
            return render(request, 'measurement/carte.html', context)
    

    carte = carte._repr_html_()
    research = SearchVehicule.objects.all()
    context = {
        'carte':carte,
        'distance':distance, 
        'temps':temps,
        'form_itineraire': form,
        'form1':form1,
        'researchs': research,
    }
    return render(request, 'measurement/carte.html', context)