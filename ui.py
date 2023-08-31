from tkinter import *
from tkinter import ttk
import database as db 
from tkinter.messagebox import askokcancel,WARNING
import helpers

#se hace una clase para poder centrar todo lo demas con la misma funcion de geometry 
class CenterWidgetMixin:
    def center(self):
        #se toma la funcion update de TK para actualizar la pantalla
        self.update()
        
        #Automatizacion del tamano de interfaz
        w=self.winfo_width()
        h=self.winfo_height()
        ws=self.winfo_screenwidth()
        hs=self.winfo_screenheight()
        
        # se toma el ancho de la pantalla y se divide entre 2 para encontrar el centro, se le resta el ancho de la ventana dividido entre 2  
        x=int(ws/2-w/2)
        #lo mismo con la altura de la pantalla
        y=int(hs/2-h/2)
        #Centrar la pantalla con geometry
        #WITHDxHEIGHTx+OFFSET_X+OFFSET_Y
        #self.geometry("500x500+500+500")
        self.geometry(f"{w}x{h}+{x}+{y}")

#Subventana de cracion e cliente
class CreateClientWindow(Toplevel,CenterWidgetMixin):
    def __init__(self,padre):
        super().__init__(padre)
        self.title("crear cliente")
        self.build()
        self.center()
        #bloquea la pantalla principal hasta no cerrar la subventana
        self.transient(padre)
        self.grab_set()
        
        
    def build(self):
        frame=Frame(self)
        frame.pack(padx=20,pady=10)    
        Label(frame,text="Id (2 ints y un char)").grid(row=0,column=0)
        Label(frame,text="Nombre (de 2 a 30 chars)").grid(row=0,column=1)
        Label(frame,text="Apellido (de 2 a 30 chars)").grid(row=0,column=2)
        
        id=Entry(frame)
        id.grid(row=1,column=0)
        id.bind("<KeyRelease>",lambda event:self.validate(event,0))
        nombre=Entry(frame)
        nombre.grid(row=1,column=1)
        nombre.bind("<KeyRelease>",lambda event:self.validate(event,1))
        apellido=Entry(frame)
        apellido.grid(row=1,column=2)
        apellido.bind("<KeyRelease>",lambda event:self.validate(event,2))
        
        frame=Frame(self)
        frame.pack(pady=10)
        crear=Button(frame,text="Crear",command=self.create_client)            
        crear.configure(state=DISABLED)
        crear.grid(row=0,column=0)
        Button(frame,text='Cancelar',command=self.close).grid(row=0,column=1,padx=10, pady=5)
        
        self.validaciones=[0,0,0]
        self.crear=crear
        self.id=id
        self.nombre=nombre
        self.apellido=apellido
        
    # def para crear cliente
    def create_client(self):
        self.master.treeview.insert(
                parent='',index='end',iid=self.id.get(),
                values=(self.id.get(),self.nombre.get(),self.apellido.get()))
        db.Clientes.crear(self.id.get(),self.nombre.get(),self.apellido.get())
        
        self.close()
    def close(self):
        self.destroy()
        self.update()
        

    '''
    def validate(self,event,index):
        
        valor=event.widget.get()
        if index==0:
            valido=helpers.dni_valido(valor,db.Clientes.lista)
            if valido:
                event.widget.configure({"bg":"Green"})
            else: 
                event.widget.configure({"bg":"Red"})
        if index==1:
            valido=valor.isalpha() and len(valor)>=2 and len(valor)<=30
            if valido:
                event.widget.configure({"bg":"Green"})
            else: 
                event.widget.configure({"bg":"Red"})
        if index==2:
            valido=valor.isalpha() and len(valor)>=2 and len(valor)<=30
            if valido:
                event.widget.configure({"bg":"Green"})
            else: 
                event.widget.configure({"bg":"Red"})
            '''
            
    def validate(self,event,index):        
        valor=event.widget.get()
        valido=helpers.dni_valido(valor,db.Clientes.lista)if index ==0 \
                else (valor.isalpha() and len(valor) >=2 and len(valor)<=30)
        event.widget.configure({"bg":"Green" if valido else "Red"})    
            
        #cambiar el estado del boton con respecto a las validaciones
        self.validaciones[index]=valido
        self.crear.config(state=NORMAL if self.validaciones == [1,1,1] else DISABLED )  
            
            
class EditClientWindow(Toplevel,CenterWidgetMixin):
    def __init__(self,padre):
        super().__init__(padre)
        self.title("Actualizar cliente")
        self.build()
        self.center()
        #bloquea la pantalla principal hasta no cerrar la subventana
        self.transient(padre)
        self.grab_set()
        
        
    def build(self):
        frame=Frame(self)
        frame.pack(padx=20,pady=10)    
        Label(frame,text="Id (No editable)").grid(row=0,column=0)
        Label(frame,text="Nombre (de 2 a 30 chars)").grid(row=0,column=1)
        Label(frame,text="Apellido (de 2 a 30 chars)").grid(row=0,column=2)
        
        id=Entry(frame)
        id.grid(row=1,column=0)
        nombre=Entry(frame)
        nombre.grid(row=1,column=1)
        nombre.bind("<KeyRelease>",lambda event:self.validate(event,0))
        apellido=Entry(frame)
        apellido.grid(row=1,column=2)
        apellido.bind("<KeyRelease>",lambda event:self.validate(event,1))
        
        cliente=self.master.treeview.focus()
        campos=self.master.treeview.item(cliente,'values')
        id.insert(0,campos[0])
        id.config(state=DISABLED)
        nombre.insert(0,campos[1])
        apellido.insert(0,campos[2])
        
        
        frame=Frame(self)
        frame.pack(pady=10)
        
        actualizar=Button(frame,text="Actualizar",command=self.edit_client) 
        actualizar.configure(state=DISABLED)           
        actualizar.grid(row=0,column=0)
        Button(frame,text='Cancelar',command=self.close).grid(row=0,column=1,padx=10, pady=5)
        
        self.validaciones=[1,1]
        self.actualizar=actualizar
        self.id=id
        self.nombre=nombre
        self.apellido=apellido
        
    # def para crear cliente
    def edit_client(self):
        cliente=self.master.treeview.focus()
        self.master.treeview.item(cliente,values=(self.id.get(),self.nombre.get(),self.apellido.get()))
        db.Clientes.modificar(self.id.get(),self.nombre.get(),self.apellido.get())
        
        self.close()
        
    def close(self):
        self.destroy()
        self.update()
            
    def validate(self,event,index):        
        valor=event.widget.get()
        valido=(valor.isalpha() and len(valor) >=2 and len(valor)<=30)
        event.widget.configure({"bg":"Green" if valido else "Red"})    
            
        #cambiar el estado del boton con respecto a las validaciones
        self.validaciones[index]=valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1,1] else DISABLED )  
                        
class MainWindow(Tk,CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes ")
        self.build()
        self.center()
    
        
    #Construccion de la interfaz   
    def build(self):
        frame=Frame(self)
        frame.pack()
        #vista en arbol 
        treeview=ttk.Treeview(frame)
        #Configurar columnas 
        treeview['columns']=('Id','Nombre','Apellido')

        #formato de las columnas 
        treeview.column("#0",width=0,stretch=NO)
        treeview.column("Id",anchor=CENTER)        
        treeview.column("Nombre",anchor=CENTER) 
        treeview.column("Apellido",anchor=CENTER) 
        #formato de cabecera
        treeview.heading("Id",text="Id",anchor=CENTER)
        treeview.heading("Nombre",text="Nombre",anchor=CENTER)
        treeview.heading("Apellido",text="Apellido",anchor=CENTER)
        #scroll
        scrollbar=  Scrollbar(frame)
        scrollbar.pack(side=RIGHT,fill=Y)
        treeview.pack()
        treeview['yscrollcommand']=scrollbar.set
        
        #agregar clientes a la interfaz
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='',index='end',iid=cliente.id,
                values=(cliente.id,cliente.nombre,cliente.apellido))     
            
        frame=Frame(self)
        frame.pack(pady=20)
        treeview.pack()
        
        Button(frame,text="Crear",command=self.create).grid(row=0,column=0,padx=10, pady=5)
        Button(frame,text="Modificar",command=self.edit).grid(row=0,column=1,padx=10, pady=5)
        Button(frame,text="Borrar",command=self.delete).grid(row=0,column=2,padx=10, pady=5)
        
        self.treeview=treeview
    def delete(self):
        
        #borra el registro que tiene el foco,subventana borrar
        cliente=self.treeview.focus()
        if cliente:
            campos=self. treeview.item(cliente,"values")
            confirmar=askokcancel(
                title="Confirmar borrado",
                message=f"Desea borrar a {campos[1]} {campos[2]}",
                icon=WARNING
            )
            if confirmar:
                self.treeview.delete(cliente)  
                db.Clientes.borrar(campos[0])
    def create(self):
        CreateClientWindow(self)
    
    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)    
            
