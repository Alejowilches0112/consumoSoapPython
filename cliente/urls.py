from django.conf.urls import url 
from cliente import views 
 
urlpatterns = [ 
    url(r'^clienteSoap/$', views.clienteSoap),
    url(r'^preoferta/$', views.obtenerPreoferta),
]