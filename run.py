#El script que pone en marcha todo 
import ui
import sys 
import Menu

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=="-t":
        Menu.iniciar()
    else:
        app=ui.MainWindow()
        app.mainloop()
    
    
    
#python run.py -t =terminal
#python run.py =interfaz