
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os;

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s se conecto." % client_address)
        client.send(bytes("Chat iniciado. Escribe tu nombre.", "utf8"))
        #Guardamos la direccion IP 
        addresses[client] = client_address
        #Usamos un hilo y lo dirigimos a la funcion, le pasamos como argumentos el sokect del cliente
        Thread(target = handle_client, args=(client,)).start()


def handle_client(client): # Toma el socket del cliente como argumento. 
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenido %s! Si quieres salir, escribe {quit}.' % name
    #Enviamos el mensaje welcome
    client.send(bytes(welcome, "utf8"))
    #Mensaje de aviso a todos los clientes
    msg = "%s se acaba de unir." % name
    broadcast(bytes(msg, "utf8"))
    #Guardamos el nombre 
    clients[client] = name

    #Enviar y revicir mensajes
    while True:
        msg = client.recv(BUFSIZ)
        if os.path.exists(msg):#Si existe el path 
             file = open('Server files/server_file.png', "wb")

             image_chunk = client.recv(BUFSIZ) 

            
             file.write(image_chunk)
                
             file.close()
             broadcast(bytes("%s: Archivo enviado" %name, "utf8"))


        elif msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            broadcast(bytes("%s se fue." % name, "utf8"))
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]#
            break

def broadcast(msg, prefix=""):
    for sock in clients:#Envia a cada cliente
        sock.send(bytes(prefix, "utf8")+msg)


#Parametros de conexion        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 5242880 #buffer
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)#

if __name__ == "__main__":
    SERVER.listen(5)
    print("Esperando conexión...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()