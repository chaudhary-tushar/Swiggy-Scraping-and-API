from django.contrib import admin
from .models import Citie as City
from .models import Restaurant

# Register your models here.

admin.site.register(City)
admin.site.register(Restaurant)
