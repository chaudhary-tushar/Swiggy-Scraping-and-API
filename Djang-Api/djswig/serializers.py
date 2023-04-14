from rest_framework import serializers
from .models import Citie,Restaurant

class cityserializer(serializers.ModelSerializer):
    class Meta:
        model = Citie
        fields =  '__all__'
    
class rest_serializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields =  '__all__'
    