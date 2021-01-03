from tkinter import Frame,Label,Button,Checkbutton,Scale,StringVar,IntVar,Entry,Tk
import serial
import time
import threading
import pandas as pd
import mysql.connector

class MainFrame(Frame):

    cad = str()
    
    def __init__(self, master=None):
        super().__init__(master, width=420, height=270)                
        self.master = master    
        self.master.protocol('WM_DELETE_WINDOW',self.askQuit)
        self.pack()        
        self.hilo1 = threading.Thread(target=self.getSensorValues,daemon=True)
        self.arduino = serial.Serial("COM3",9600,timeout=1.0)
        time.sleep(1)
        self.value_temp_1 = IntVar()
        self.value_temp=StringVar()
        self.nombreA = StringVar()
        self.apelli=StringVar()
        self.age=IntVar()
        self.dato=IntVar()
        self.create_widgets()
        self.isRun=True
        self.hilo1.start()
        self.enviar()
        self.cad= str()
        self.cnn=mysql.connector.connect(host="localhost",user="root",passwd="",database="historial") #Conectar con MySQL
        print(self.cnn)
    def Enviar_db(self):
        
         
        cur=self.cnn.cursor()
        sql="INSERT INTO historialmedico (Nombre,Apellido,Edad,Temperatura)VALUES('{}','{}','{}','{}')".format(self.nombreA.get(),self.apelli.get(),self.age.get(),self.value_temp_1)
        cur.execute(sql)
        self.cnn.commit()
        time.sleep(1)
        cur.close()
            
    def askQuit(self):
        self.isRun=False
        self.arduino.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print("*** finalizando...")

    def getSensorValues(self):
    
        while self.isRun:
            cad =self.arduino.readline().decode('ascii').strip()
            self.value_temp.set(cad)
            self.value_temp_1=float(cad)
            
    def enviar(self):
        x= (self.cad)
        print(x)
        datos= list()

    def create_widgets(self):
        self.labelBPM= Label(self,text = "Nombre: ", bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=9 ,justify="center")
        self.labelBPM.pack()
        self.labelBPM.grid(row=0,column=0, padx=5,ipady=8, pady=10)
        
        self.label1= Entry(self, textvariable=self.nombreA,   bg= "red",fg="black", font="Helvetica 13 bold",width=15 ,justify="center")
        self.label1.grid(row=0,column=1, padx=5,ipady=8, pady=10)        
        
        self.labelapellido= Label(self,text = "Apellido: ", bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=9 ,justify="center")
        self.labelapellido.grid(row=1,column=0, padx=5,ipady=8, pady=10)
        
        self.label2= Entry(self,textvariable=self.apelli,bg= "red",fg="black", font="Helvetica 13 bold",width=15 ,justify="center")
        self.label2.grid(row=1,column=1, padx=5,ipady=8, pady=10)        
        
        self.labeledad= Label(self,text = "Edad: ", bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=9 ,justify="center")
        self.labeledad.grid(row=2,column=0, padx=5,ipady=8, pady=10)
        
        self.label3= Entry(self,textvariable=self.age, bg= "red",fg="black", font="Helvetica 13 bold",width=15 ,justify="center")
        self.label3.grid(row=2,column=1, padx=5,ipady=8, pady=10)        
        
        self.Limpiar= Button(self,command= self.Enviar_db, text= "Enviar historial ",bg="blue",fg="white", font="Helvetica 14 bold",width=20,justify="center")
        self.Limpiar.pack
        self.Limpiar.grid(row=3,column=0, padx=5,pady=15,columnspan=2)
        
        self.labelT= Label(self,textvariable = self.value_temp, bg= "yellow",fg="black", font="Helvetica 13 bold",width=9 ,justify="center")
        self.labelT.grid(row=0,column=2, padx=5,ipady=8, pady=10)
        
        self.Limpiar1= Button(self,command= self.askQuit, text= "Salir ",bg="red",fg="white", font="Helvetica 14 bold",width=7,justify="center")
        self.Limpiar1.pack
        self.Limpiar1.grid(row=3,column=3, padx=5,pady=15,columnspan=2)        
        
def main():
    root = Tk()
    root.wm_title("Monitoro del signo vital de la temperatura")
    app = MainFrame(root)
    app.mainloop()

if __name__=="__main__":
    main()        
