from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework import status
# Create your views here.
from suds.client import Client
from xml.etree.ElementTree import XML, fromstring
import base64
import os
import pandas as pd

@csrf_exempt
def clienteSoap(request):
    print(request)
    if request.method == 'GET':
        client = Client(url='https://dialogo.clientesbayport.com/serviciosTest/index.php/servicio?wsdl')
        usuario = "P4TZU"
        clave= "P3Fwfv8lmy"
        #data = JSONParser().parse(request)
        #carpeta = data['carpeta']
        detalle = ''
        tramites = [

            {'tramite': '584057', 'formato': '5'},
            {'tramite': '584060', 'formato': '5'}
        ]
        x=0
        for i in tramites: 
            try:
                x=x+1
                tramite = i
                print("PETICION "+ str(x) +" EN PROCESO")
                response = client.service.GetFormatoPdf(usuario, clave, tramite['tramite'], tramite['formato'], '123', 11001,'13/10/2020')
                print(response)
                myxml = fromstring(response)
                if(myxml.find('codigo').text in '01'):
                    pdf64 = myxml.find('pdf').text
                    pdf = base64.b64decode(pdf64)
                    nombrePdf = 'tramite-'+tramite['tramite']
                    with open(os.path.expanduser('pdfs/'+nombrePdf+'.pdf'), 'wb') as fout:
                        fout.write(pdf)
                        fout.close()
                else:
                    detalle = detalle+'\n'+myxml.find('detalle').text+' '+tramite['tramite']+ ' peticion: '+str(i)
                print("PETICION "+str(x)+" FINALIZADA")
            except Exception as err:
                print("Encountered exception. {}".format(err))
        
        with open(os.path.expanduser('errores.txt'), 'w') as ferr:
            ferr.write(detalle)
            ferr.close()
        return JsonResponse({"codigo": "01"})

@csrf_exempt
def obtenerPreoferta(request):
    if request.method == 'GET':
        client = Client(url='https://dialogo.clientesbayport.com/servicios_retencion/index.php/servicio?wsdl')
        usuario = "R3T3NC10N"
        contrasena = "KSH05opl96Jy2"
        #resp = []
        try:
            df = pd.read_csv("C:/Users/Administrador/Documents/dlg_preoferta_retencion.csv",encoding="iso-8859-1", delimiter=";")
            df.head(100)
            for data in df["NUMERO_DOCUMENTO"]:
                print(data)
                response = client.service.ObtenerPreOferta(usuario,contrasena,data)
                myxml = fromstring(response)
                print(myxml.find('detalle').text)
                #resp[data] = {"codigo":  myxml.find('codigo').text, "detalle":  myxml.find('detalle').text}
            return JsonResponse({"codigo": "01"})
        except Exception as err:
            print("Encountered exception. {}".format(err))
