#our helperfunctions 
from curses import noecho
from django.contrib.gis.geoip2 import GeoIP2
import socket


def get_user_ip():
    ip =  socket.gethostbyname_ex(socket.gethostname())[2]
    if "127.0.0.1" is not ip:
        return ip 
    else:
        return '12.56.25.5'



def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat , lon = g.lat_lon(ip)
    return  country, city, lat, lon


def get_center_cooordinates(laA:float,loA:float,laB:float=None,loB:float=None):
    coords = (laA, loA)
    if laB:
        coords1 =(laA+loA)/2
        coords2 = (loB+loB)/2
        
        return (coords1, coords2)
    
    
def get_zoom(distance):
    if(distance<100):
        return 8
    
    elif(100<distance and distance<500):
        return 4
    
    else:
        return 2 
    
    
    
    
def visitor_ip_address(request):
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip