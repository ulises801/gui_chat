
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter.filedialog import askopenfilename
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            
            if "Archivo enviado" in msg: #Lalo: Archivo enviado
                
                link = tkinter.Label(messages_frame,text="Descargar", fg="blue", cursor="hand2")
                link.pack()
                link.bind("<Button-1>", download)

                msg_list.insert(tkinter.END, msg)

            elif msg == "Enviando":
                #Inserta el mensaje en la interfaz
                file = open('Client files/client_file.png', "wb")

                image_chunk = client_socket.recv(BUFSIZ) 
            
                file.write(image_chunk)
                
                file.close()
                msg_list.insert(tkinter.END, "Descarga completada")
            else:
                #Inserta el mensaje en la interfaz
                msg_list.insert(tkinter.END, msg)
        except OSError:  
            print(OSError)
            break

def send(event=None):#Funcion ligada a un boton

    msg = my_msg.get()#Obtenemos el mensaje desde la interfaz
    my_msg.set("")#Deja en blanco el cuadro de texto
    client_socket.send(bytes(msg, "utf8"))

    if msg == "{quit}":

        client_socket.close()#Cerrar conexion
        top.quit()#Cerrar aplicacion

def send_file(event=None):

    path = my_file.get()#Obtenemos el path desde la interfaz
    my_file.set("")

    #root, extension =os.path.splitext(path_Inicio)
    # path = askopenfilename()
    # path.replace("\\","/")
    # print (path)
    client_socket.send(bytes(path, "utf8"))#C:/Users/eduar/Downloads/Rinnegan_de_Sasuke.png

    #Enviar el archivo
    file = open(path, 'rb')

    file_data  = file.read(BUFSIZ)

    
    client_socket.send(bytes(file_data))
    
    
    file.close()
    print("-----------------------------------")


def download(event=None):

    path = "download"
    client_socket.send(bytes(path, "utf8"))

    

def on_closing(event=None):

    my_msg.set("{quit}")
    send()

#GUI
top = tkinter.Tk()
top.title("Chat")

messages_frame = tkinter.Frame(top)#Definimos un area para el chat 
my_msg = tkinter.StringVar() 
my_msg.set("Escribe aqui")
my_file = tkinter.StringVar() 
my_file.set("Direccion del archivo")
scrollbar = tkinter.Scrollbar(messages_frame) 

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)#Esto como tal seria el chat
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)#Campo de texto mensajes
entry_field.bind("<Return>", send)#Para poder utlizar ENTER
entry_field.pack()
send_button = tkinter.Button(top, text="Enviar", command=send)#Boton enviar, con la funcion send
send_button.pack()

entry_field = tkinter.Entry(top, textvariable=my_file)#Archivos
entry_field.bind("<Return>", send_file)
entry_field.pack()
send_button = tkinter.Button(top, text="Enviar archivo", command=send_file)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)#Boton de cerrar

#Parametros de conexion
HOST = '127.0.0.1'
PORT = '33000'
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 5242880 #buffer
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)#

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()



#C:/Users/vgonz/OneDrive/Im??genes/david 4.png