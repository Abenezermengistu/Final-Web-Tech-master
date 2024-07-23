import requests
from django.http import HttpResponse
from django.template import loader
from geolocation.models import UserConnection
import json
import os




def get_geolocation_data(request):
    """
    We extract the client ip and send it
    through a get request to an external API which
    returns the geolocation data of the ip.
    """
    
    ip_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    api_secret_key = os.getenv('API_SECRET_KEY')
    if not ip_addr:
        ip_addr = request.META.get('REMOTE_ADDR')
    s = rf'http://api.ipstack.com/{ip_addr}?access_key={api_secret_key}'
    r = requests.get(s)
    geolocation_data = json.loads(r.content.decode('utf-8'))
    return geolocation_data

def update_geolocation_db(ip):
    """
    We want to compare the client's ip to the
    ones already in the db. If the client's ip 
    is already present we increment the num_conn attribute
    otherwise we add a new row.
    """

    client_obj, created = UserConnection.objects.get_or_create(user_ip = ip)
    if not created:
        #old client
        client_obj.num_conn += 1
        client_obj.save()


# Create your views here.

def index(request):
    geolocation_data = get_geolocation_data(request)
    update_geolocation_db(geolocation_data['ip'])    

    client_data = [str(k)+': '+str(geolocation_data[k]) for k in geolocation_data.keys()]
    
    template = loader.get_template('geolocation/index.html')
    context = {'client_data': client_data}
    
    return HttpResponse(template.render(context, request))


def user_history(request):
    #get client ip address
    ip_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    if not ip_addr:
        ip_addr = request.META.get('REMOTE_ADDR')
    #user_ip is primary key of the db, so only one row will be retrieved
    qs = UserConnection.objects.filter(user_ip = ip_addr)
    for row in qs:
        user_conn = row.num_conn
    template = loader.get_template('geolocation/user_history.html')
    context = {'user': user_conn}
    return HttpResponse(template.render(context, request))
