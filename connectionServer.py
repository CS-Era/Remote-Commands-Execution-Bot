from socket import *
from tqdm import tqdm
from colorama import Fore
from time import sleep


IP = "192.168.1.52"
PORT = 12000
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"


# OK crea connessione
def serverConnection():
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(ADDR)
        server.listen(1)
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