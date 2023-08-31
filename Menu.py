#Interfaz de proyecto
import os 
import helpers
import database as db

def iniciar():
    while True:
    
    # para limpiar ,cls es clean screen LLAMANDO A HELPERS 
        helpers.limpiar_Pantalla ()
    
    #Crear el menu 
        print('============================')
        print("    Bienvenido al gestor    ")
        print('============================')
        print("  [1] Listar los clientes   ")
        print("  [2] Buscar un cliente     ")
        print("  [3] Crear un cliente      ")
        print("  [4] Modificar un cliente  ")
        print("  [5] Borrar un cliente     ")
        print("  [6] Salir                 ")
        print('============================')
    
    
        opcion=input(">")
        helpers.limpiar_Pantalla ()
    
        #Comprobacion de la opcion 
        if opcion =='1':
            print("Listando los clientes... \n ")
            for cliente in db.Clientes.lista:
                print(cliente)
            
        elif opcion =='2':
            print("Buscando al cliente...   \n ")
            id=helpers.leer_texto(3,3,"id(2 ints y un char)").upper()
            cliente=db.Clientes.buscar(id)
            print(cliente) if cliente else print("Cliente no encontrado")
            
        elif opcion =='3':
            print("Creando al cliente...    \n ")
            id=None
            while True:
                    id=helpers.leer_texto(3,3,"id(2 ints y un char)").upper()
                    if helpers.dni_valido(id,db.Clientes.lista):
                        break
            nombre=helpers.leer_texto(2,30,"nombre(de 2 a 30 chars)").capitalize()
            apellido=helpers.leer_texto(2,30,"apellido(de 2 a 30 chars)").capitalize()
            db.Clientes.crear(id,nombre,apellido)
            print("Cliente anadido correctamente")
            
        elif opcion =='4':
            print("Modificando al cliente...\n ")
            id=helpers.leer_texto(3,3,"id(2 ints y un char)").upper()
            cliente=db.Clientes.buscar(id)
            if cliente:
                nombre=helpers.leer_texto(2,30,f"nombre(de 2 a 30 chars)[{cliente.nombre}]").capitalize()
                apellido=helpers.leer_texto(2,30,f"apellido(de 2 a 30 chars)[{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.id,nombre,apellido)
                print("Cliente modificado correctamente")
            else:
                print("Cliente no encontrado")    
                

        elif opcion =='5':
            print("Borrando un cliente...   \n ")
            id=helpers.leer_texto(3,3,"id(2 ints y un char)").upper()
            print("Cliente borrado correctamente")if db.Clientes.borrar(id) else print("Cliente no encontrado ")
            
            
        elif opcion =='6':
            print("Saliendo del programa... \n ")
            break 
        input("\nPresiona ENTER para continuar...")      