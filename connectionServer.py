from socket import *
from tqdm import tqdm
from colorama import Fore
from time import sleep



IP = "localhost"
PORT = 12001  # Porta di 2Ascolto del TCP
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
fileLog = f"###          FILELOG RESULT          ###\n"


# OK crea connessione
def serverConnection():
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(ADDR)
        server.listen(5)
        print()
        for i in tqdm(range(20), desc=Fore.LIGHTWHITE_EX + "[STARTING] Starting the server...", colour="green", ncols=65,
                      bar_format="{desc}: {percentage:3.0f}% {bar}"):
            sleep(0.2)
        print(f"[LISTENING] The Sever is waiting for a victim...\n")
        return server
    except:
        #traceback.print_exc()
        print(f"[ERROR] Unable to start the Server...\n")
        return "errore"