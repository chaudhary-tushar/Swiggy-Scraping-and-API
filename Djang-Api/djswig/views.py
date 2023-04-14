from django.shortcuts import render
from django.urls import reverse_lazy as reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import cityserializer,rest_serializer
from .models import Citie,Restaurant
import random

cities=['ahmedabad','mumbai','gurgaon','hyderabad','kolkata','bangalore','delhi','chennai']


@api_view (['GET'])
def ShowAll(request):
    cities= Citie.objects.all()
    serializer =cityserializer(cities, many=True)
    return Response(serializer.data)

@api_view (['GET'])
def ShowAllres(request):
    rests= Restaurant.objects.all()[:100]
    serializer =rest_serializer(rests, many=True)
    return Response(serializer.data)

@api_view (['GET'])
def topres(request,city):
    rests = Restaurant.objects.filter(city_name=city).order_by('-ratings')[:10]
    serializer= rest_serializer(rests,many=True)
    return Response(serializer.data)

def tapi_view(request):
    city_name=random.choice(cities)
    apis = [
        {'name': 'CITY-LIST API','url': 'http://127.0.0.1:8000/tapi/city-list/','description': 'API for retrieving cities listed',},
        {'name': 'RESTAURANTS API','url': 'http://127.0.0.1:8000/tapi/rest-list/','description': 'API for retrieving restaurants',},
        {'name': 'TOPRES API','url': f'http://127.0.0.1:8000/tapi/top-res/{city_name}','description': 'API for retrieving top 10 restaurants in a city',}
    ]
    context={'apis':apis}
    return render(request, 'tapi.html', context)
    