from django.urls import path
from . import views

app_name = 'djswig'
urlpatterns = [
    path('', views.tapi_view, name='djswig'),
    path('city-list/',views.ShowAll,name='city-list'),
    path('rest-list/',views.ShowAllres,name='rest-list'),
    path('top-res/<str:city>',views.topres,name='top-res'),
]
