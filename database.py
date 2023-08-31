import csv
import config
#Este fihero contiene datos ademas de funciones como modificar, borrar y crear 

#Clase que maneja un cliente,lo crea
class Cliente():
    def __init__(self,id,nombre,apellido):
        self.id=id
        self.nombre=nombre
        self.apellido=apellido
        
    def __str__(self) :
        return f"({self.id}){self.nombre}{self.apellido}"    

#Hace una lista de clientes en general 
class Clientes(): 
    lista=[]
    with open (config.DATABASE_PATH,newline='\n')as fichero:
        reader=csv.reader(fichero,delimiter=';')
        for id,nombre,apellido in reader:
            cliente=Cliente(id,nombre,apellido)
            lista.append(cliente)
        
    # El metodo estatico permite tomar el resultado de las funciones sin necesidad de llamar a todo el metodo o funcion.
    #metodo estatico buscar 
    @staticmethod
    # recorre la lista y busca los clientes 
    def buscar(id):
        for cliente in Clientes.lista:
            if cliente.id == id:
                return cliente
    
    #metodo estatico crear 
    @staticmethod
    def crear(id,nombre,apellido):
        #Crea la instancia de la clase cliente con el id, nombre y apellido 
        cliente=Cliente(id,nombre,apellido)
        #anade en la lista 
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente
    
    #metodo estatico modificar
    @staticmethod
    def modificar(id,nombre,apellido):
        #Se hace un indice para poder recuperar datos 
        #El enumerate permite recibir esos indices 
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.id == id:
                #hace referencia al indice y poscicion
                Clientes.lista[indice].nombre=nombre
                Clientes.lista[indice].apellido=apellido
                Clientes.guardar()
                #retorna el objeto en la poscicion
                return  Clientes.lista[indice]
            
    #metodo estatico Eliminar
    @staticmethod
    def borrar(id):
    #recorrer la lista con un for 
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.id == id:
                cliente= Clientes.lista.pop(indice)
                Clientes.guardar()
                #se realiza un pop al indice para borrar 
                return cliente
            
    #metodo estatico guardar en archivo csv
    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH,'w',newline='\n') as fichero:
            writer=csv.writer(fichero,delimiter=';')
            for cliente in Clientes.lista:
                writer.writerow((cliente.id,cliente.nombre,cliente.apellido))