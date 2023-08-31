#Contiene funciones auxiliares de uso general
import os
import platform
import re 

def limpiar_Pantalla(): 
    #Funciones avanzados, para poder limpiar la pantalla
    os.system('cls') if platform.system()=="Windows" else os.system('clear')


def leer_texto(longitud_min=0,longitud_max=100,mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto=input(">")
        if len(texto)>= longitud_min and len(texto)<= longitud_max:
            return texto

#validacion del id 

def dni_valido(id,lista):
    # si no concuerda con el re match
    if not re.match('[0-9]{2}[A-Z]$',id):
        print("ID incorrecto debe de cumplir con el formato")  
        return False

    for cliente in lista:
        if cliente.id==id:
            print("Id utilizado por otro cliente")
            return False
    return True
