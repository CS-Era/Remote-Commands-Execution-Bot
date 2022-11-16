from socket import *
import socket
import signal

IP = "localhost"
PORT = 12001
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"


#gestisce il ctrl-C per l'uscita
def signalHandler(signum,frame):
    msg="Uscita effettuata con successo"
    print(":",msg,end="",flush=True)
    exit(1)

def serverConnection():
    try:
        server=socket(AF_INET,SOCK_STREAM)
        server.bind(ADDR)
        server.listen(1)
        print(f"\n[LISTENING] Server is up and it's waiting for a client connection")
    except:
        print(f"[ERROR] Connection refused")
        exit(1)
    return server


#lista dei comandi disponibili per il controllo remoto
def commandsHelp():
    print("#####    Comandi disponibili     ####")
    print()
    print("Download di file:    download <nomeFile.estensione>")
    print("Mostra Working Directory:    pwd")
    print("Lista dei file in un percorso:   ls")
    print("Lista di tutti i file (compresi i nascosti) in un percorso:  ls -a")
    print("Cambia posizione:    cd <path>")
    print("Cerca un file in tutto il FileSystem:   find <nomeFile.estensione>")
    print("Cerca un file nel path desiderato:   find <nomeFile.estensione> <Path>")
    print("Effettua screenshot:     screenshot")
    print("Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <nomeFiletxt> <estensione>")
    print("Esci dal controllo remoto:   exit")
    print()
    print("####################################")


def printInformazioni(clientConnection):

    #Ricezione del file dal Client
    buff=1
    risposta="y"
    nbytes=clientConnection.recv(1024).decode(FORMAT)
    print(nbytes)

    while buff and nbytes != '':
        buff=clientConnection.recv((int(nbytes)+1)).decode(FORMAT)
        nbytes=''
        if buff[0:7] == "[ERROR]":
            risposta=input(buff)
            clientConnection.send((risposta).encode(FORMAT))
            if risposta == "Y" or risposta == "y":
                buff = 1
            elif risposta == "N" or risposta == "n":
                buff = 0
                break

        print(buff)

    if risposta == "Y" or risposta == "y":
        print(f"[RECEIVING] File 'OperatingSystem.txt' received: Find all useful information on the client's operating system.\n")
    elif risposta == "N" or risposta == "n":
        print(f"[RECEIVING] File 'OperatingSystem.txt' not received.\n")

    return "finito"


def main():
    signal.signal(signal.SIGINT, signalHandler)
    exit = False
    server = serverConnection()

    while exit == False:

        clientConnection, addr = server.accept()
        print(f"[CONNECTED] Client {addr} is connected to the server")
        print()

        # ricevo info sul sistema
        OSInfo = clientConnection.recv(1024).decode()

        print(f"System's Information received:\n")
        print(OSInfo + "\n")
        time.sleep(4)
        print("[REMOTE CONTROL] Starting procedure...")
        time.sleep(4)
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

