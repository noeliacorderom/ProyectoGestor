import copy
import unittest
import database as db
import helpers
import config 
import csv 
#Clase para todos los test que se haran 
class TestData(unittest.TestCase):
    def setUp(self):
        # Antes de ejecutar cada prueba se le pasara a la lista una serie de clientes por medio de la bd
        db.Clientes.lista=[
            #Mokup objects,objeto de prueba para los test
        db.Cliente('15J','Noelia','Cordero'),
        db.Cliente('48H','Sebastian','Mora'),
        db.Cliente('34M','Yenori','Morales')
        ]
    
    #Comprobar que funciona la funcion de buscar '
    def test_buscar_cliente(self):
        cliente_existente=db.Clientes.buscar('15J')
        cliente_inexistente=db.Clientes.buscar('15m')
        
        #comprobacion de la existencia o no existencia de un cliente por medio del None
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
        
    #Comprobar que funciona la funcion de crear
    def test_crear_cliente(self):
        nuevo_cliente=db.Clientes.crear('46J','Noe','Morales')
        self.assertEqual(len(db.Clientes.lista),4)
        #Comproband cada poscicion
        self.assertEqual(nuevo_cliente.id,'46J')
        self.assertEqual(nuevo_cliente.nombre,'Noe')
        self.assertEqual(nuevo_cliente.apellido,'Morales')
        
    #Comprobar que funciona la funcion de modificar
    def test_modificar_cliente(self):
        #Buscar un cliente y crear una copia del mismo
        cliente_a_modificar=copy.copy(db.Clientes.buscar('48H'))
        # nos permite modificar
        cliente_modificado=db.Clientes.modificar('48H','Alberto','Mora')
        #comprobar el nombre a odificar 
        self.assertEqual(cliente_a_modificar.nombre,'Sebastian')
        self.assertEqual(cliente_modificado.nombre,'Alberto')
        
    #Comprobar que funciona la funcion de eliminar
    def test_borrar_cliente(self):
        cliente_borrado=db.Clientes.borrar('34M')
        #primero se busca el cliente 
        cliente_rebuscado=db.Clientes.buscar('34M')
        self.assertEqual(cliente_borrado.id,'34M')
        self.assertIsNone(cliente_rebuscado) 
        
        
    #Test para validar dni invalido
    
    def test_id_valido(self):
        self.assertTrue(helpers.dni_valido('15A',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('111112222',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F55',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('15J',db.Clientes.lista))
        
    def test_escritura_csv(self):
        db.Clientes.borrar('15J')   
        db.Clientes.borrar('48H')
        db.Clientes.modificar('34M','Maria','Mora')
        id,nombre,apellido=None,None,None
        with open(config.DATABASE_PATH,newline='\n') as fichero:
            reader=csv.reader(fichero,delimiter = ";")
            id,nombre,apellido=next(reader)
            # comprobacion del unico archivo que debe de quedar en la bd
            self.assertEqual(id,'34M')
            self.assertEqual(nombre,'Maria')
            self.assertEqual(apellido,'Mora')